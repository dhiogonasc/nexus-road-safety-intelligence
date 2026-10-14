import sys
import duckdb
from config import settings


def test_duckdb_postgres_connection():

    print("\n" + "=" * 100)
    print(f" DUCKDB -> POSTGRES ({settings.ENV.upper()})")
    print("=" * 100)
    print(f"• Ambiente:   {settings.ENV}")
    print(f"• Host:       {settings.DB_HOST}")
    print(f"• Porta:      {settings.DB_PORT}")
    print(f"• Banco:      {settings.DB_NAME}")
    print(f"• Usuário:    {settings.DB_USER}")
    print(f"• SSL Mode:   {'require' if settings.ENV == 'prod' else 'prefer'}")

    try:
        conn = duckdb.connect()
        conn.execute("INSTALL postgres;")
        conn.execute("LOAD postgres;")

        conn_str = settings.postgres_conn_string
        print("-" * 100)
        print(f"• Anexando banco PostgreSQL no DuckDB...")
        conn.execute(f"ATTACH '{conn_str}' AS pg_db (TYPE POSTGRES);")

        version = conn.execute("SELECT version();").fetchone()[0]
        print(f" SUCCESS: Conexão DuckDB estabelecida!")
        print(f"   └─ Versão PG: {version[:65]}...")

        schemas = conn.execute(
            "SELECT schema_name FROM information_schema.schemata WHERE catalog_name = 'pg_db';"
        ).fetchall()
        schema_list = [s[0] for s in schemas]
        print(f"   └─ Schemas detectados: {schema_list}")

        conn.execute("DETACH pg_db;")
        conn.close()
        return True

    except Exception as e:
        print(f" ERROR: Falha na conexão via DuckDB ao ambiente {settings.ENV.upper()}")
        print(f"   └─ Detalhe do Erro: {e}")
        return False


if __name__ == "__main__":
    duck_ok = test_duckdb_postgres_connection()

    print("-" * 100)
    if duck_ok:
        print(f" RESULTADO: Todos os testes passaram para o ambiente {settings.ENV.upper()}!")
        print("=" * 100)
        sys.exit(0)
    else:
        print(f" RESULTADO: Ocorreram falhas no teste do ambiente {settings.ENV.upper()}.")
        print("=" * 100)
        sys.exit(1)