"""test_storage.py"""

import sys
import duckdb
from config import settings


def test_duckdb_storage_connection():

    print("\n" + "=" * 100)
    print(f" DUCKDB -> SUPABASE STORAGE ({settings.ENV.upper()})")
    print("=" * 100)
    print(f"• Ambiente:   {settings.ENV}")
    print(f"• Bucket:     {settings.STORAGE_BUCKET}")
    print(f"• Endpoint:   {settings.STORAGE_ENDPOINT}")
    print(f"• Região:     {settings.STORAGE_REGION}")

    try:
        conn = duckdb.connect()
        conn.execute("INSTALL httpfs;")
        conn.execute("LOAD httpfs;")
        conn.execute("INSTALL parquet;")
        conn.execute("LOAD parquet;")

        print("-" * 100)
        print(f"• Configurando segredo S3 no DuckDB...")
        
        # Teste alterando URL_STYLE entre 'path' e 'vhost' se persistir erro 404
        conn.execute(f"""
            CREATE OR REPLACE SECRET "test_supabase_secret" (
                TYPE S3,
                PROVIDER CONFIG,
                KEY_ID '{settings.STORAGE_ACCESS_KEY_ID}',
                SECRET '{settings.STORAGE_SECRET_ACCESS_KEY}',
                REGION '{settings.STORAGE_REGION}',
                ENDPOINT '{settings.STORAGE_ENDPOINT}',
                URL_STYLE 'path'
            );
        """)

        print(f"• Criando tabela de teste local...")
        conn.execute("CREATE TABLE teste_storage_conexao (id INTEGER, mensagem VARCHAR);")
        conn.execute("INSERT INTO teste_storage_conexao VALUES (1, 'Teste de conexão com Supabase Storage OK!');")

        target_url = f"s3://{settings.STORAGE_BUCKET}/teste/conexao_teste.parquet"
        print(f"• Gravando arquivo Parquet de teste em: {target_url}")
        
        conn.execute(f"""
            COPY teste_storage_conexao TO '{target_url}' (FORMAT PARQUET, OVERWRITE_OR_IGNORE 1);
        """)

        print(f" SUCCESS: Conexão e escrita no Supabase Storage estabelecidas com sucesso!")

        conn.close()
        return True

    except Exception as e:
        print(f" ERROR: Falha ao conectar no Storage via DuckDB no ambiente {settings.ENV.upper()}")
        print(f"   └─ Detalhe do Erro: {e}")
        return False


if __name__ == "__main__":
    storage_ok = test_duckdb_storage_connection()

    print("-" * 100)
    if storage_ok:
        print(
            f" RESULTADO: Todos os testes de storage passaram para o ambiente {settings.ENV.upper()}!"
        )
        print("=" * 100)
        sys.exit(0)
    else:
        print(
            f" RESULTADO: Ocorreram falhas no teste de storage do ambiente {settings.ENV.upper()}."
        )
        print("=" * 100)
        sys.exit(1)