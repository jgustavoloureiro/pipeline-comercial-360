import pandas as pd


arquivos_gold = {
    "KPIs Comerciais": "data/gold/gold_kpis_comerciais.parquet",
    "Funil Comercial": "data/gold/gold_funil_comercial.parquet",
    "Pipeline por Produto": "data/gold/gold_pipeline_produto.parquet"
}


for nome, caminho in arquivos_gold.items():
    print("=" * 80)
    print(nome)
    print("=" * 80)

    df = pd.read_parquet(caminho)

    print(f"Arquivo: {caminho}")
    print(f"Linhas: {len(df)}")
    print(f"Colunas: {len(df.columns)}")

    print("\nColunas:")
    for coluna in df.columns:
        print(f"- {coluna}")

    print("\nPrimeiras linhas:")
    print(df.head())

    print("\n")