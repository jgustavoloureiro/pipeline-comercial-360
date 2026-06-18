import duckdb
from pathlib import Path


def criar_banco_analytics():
    database_dir = Path("database")
    database_dir.mkdir(parents=True, exist_ok=True)

    database_path = database_dir / "comercial_analytics.duckdb"

    con = duckdb.connect(str(database_path))

    # Views Gold Analítica
    con.execute("""
        CREATE OR REPLACE VIEW vw_gold_kpis_comerciais AS
        SELECT *
        FROM read_parquet('data/gold/gold_kpis_comerciais.parquet')
    """)

    con.execute("""
        CREATE OR REPLACE VIEW vw_gold_funil_comercial AS
        SELECT *
        FROM read_parquet('data/gold/gold_funil_comercial.parquet')
    """)

    con.execute("""
        CREATE OR REPLACE VIEW vw_gold_pipeline_produto AS
        SELECT *
        FROM read_parquet('data/gold/gold_pipeline_produto.parquet')
    """)

    # Views Gold Dimensional
    con.execute("""
        CREATE OR REPLACE VIEW vw_dim_tempo AS
        SELECT *
        FROM read_parquet('data/gold/dim_tempo.parquet')
    """)

    con.execute("""
        CREATE OR REPLACE VIEW vw_dim_produto AS
        SELECT *
        FROM read_parquet('data/gold/dim_produto.parquet')
    """)

    con.execute("""
        CREATE OR REPLACE VIEW vw_dim_regiao AS
        SELECT *
        FROM read_parquet('data/gold/dim_regiao.parquet')
    """)

    con.execute("""
        CREATE OR REPLACE VIEW vw_dim_canal AS
        SELECT *
        FROM read_parquet('data/gold/dim_canal.parquet')
    """)

    con.execute("""
        CREATE OR REPLACE VIEW vw_dim_segmento AS
        SELECT *
        FROM read_parquet('data/gold/dim_segmento.parquet')
    """)

    con.execute("""
        CREATE OR REPLACE VIEW vw_fato_comercial AS
        SELECT *
        FROM read_parquet('data/gold/fato_comercial.parquet')
    """)

    print("Banco DuckDB criado/atualizado com sucesso.")
    print(f"Arquivo: {database_path}")

    print("\nViews criadas:")
    views = con.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'main'
        ORDER BY table_name
    """).df()

    print(views)

    con.close()


if __name__ == "__main__":
    criar_banco_analytics()