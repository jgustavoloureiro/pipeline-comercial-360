import pandas as pd

arquivo = "data/raw/base_comercial_funil_360.xlsx"

excel = pd.ExcelFile(arquivo)

print("Abas encontradas:")

for aba in excel.sheet_names:
    df = pd.read_excel(arquivo, sheet_name=aba)
    print(f"- {aba}: {len(df)} linhas e {len(df.columns)} colunas")
    