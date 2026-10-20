"""test_pipeline_copy.py"""

import os
import duckdb
from dotenv import load_dotenv

load_dotenv(".env.dev")

access_key = os.getenv("STORAGE_ACCESS_KEY_ID")
secret_key = os.getenv("STORAGE_SECRET_ACCESS_KEY")
endpoint = os.getenv("STORAGE_ENDPOINT")
region = os.getenv("STORAGE_REGION")
bucket = os.getenv("STORAGE_BUCKET")

print(f"A testar cópia para o bucket: {bucket}")
print(f"Endpoint: {endpoint}")

conn = duckdb.connect()

# Instala extensões
conn.execute("INSTALL httpfs; LOAD httpfs;")
conn.execute("INSTALL parquet; LOAD parquet;")

# Cria o secret exatamente como no pipeline
conn.execute(f"""
    CREATE OR REPLACE SECRET "test_pipeline_secret" (
        TYPE S3,
        PROVIDER CONFIG,
        KEY_ID '{access_key}',
        SECRET '{secret_key}',
        REGION '{region}',
        ENDPOINT '{endpoint}',
        URL_STYLE 'path'
    );
""")

try:
    # Simula a tabela stage de acidentes/ocorrencias
    conn.execute("CREATE SCHEMA \"bronze\";")
    conn.execute("CREATE TABLE \"bronze\".\"ocorrencias\" (id INTEGER, arquivo_fonte VARCHAR, data_carga DATE);")
    conn.execute("INSERT INTO \"bronze\".\"ocorrencias\" VALUES (1, 'datatran2026.csv', '2026-10-20');")

    # Testa exatamente a query COPY com a estrutura /bronze/acidentes/ocorrencias/
    target_query = f"""
        COPY "bronze"."ocorrencias" TO 's3://{bucket}/bronze/acidentes/ocorrencias/' (
            FORMAT PARQUET,
            PARTITION_BY (arquivo_fonte, data_carga),
            OVERWRITE_OR_IGNORE 1
        );
    """
    
    print("A executar o COPY com particionamento...")
    conn.execute(target_query)
    print("Sucesso total na cópia com particionamento!")

except Exception as e:
    print("\n[ERRO] Falha na execução:")
    print(e)

finally:
    conn.close()