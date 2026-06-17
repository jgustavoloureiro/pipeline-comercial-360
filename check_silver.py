import pandas as pd

df = pd.read_parquet("data/silver/silver_comercial.parquet")

print("Primeiras 5 linhas da Silver:")
print(df.head())

print("\nColunas da Silver:")
for coluna in df.columns:
    print(f"- {coluna}")

print("\nResumo técnico:")
print(df.info())

print("\nQuantidade de nulos por coluna:")
print(df.isna().sum())