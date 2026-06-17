from pathlib import Path
import pandas as pd


def padronizar_nome_coluna(nome: str) -> str:
    """
    Padroniza nomes de colunas para um formato mais amigável para engenharia de dados.
    Exemplo: 'Receita Consolidada' -> 'receita_consolidada'
    """
    nome = str(nome).strip().lower()
    nome = nome.replace(" ", "_")
    nome = nome.replace("-", "_")
    nome = nome.replace("/", "_")
    nome = nome.replace(".", "")
    nome = nome.replace("ç", "c")
    nome = nome.replace("ã", "a")
    nome = nome.replace("á", "a")
    nome = nome.replace("à", "a")
    nome = nome.replace("â", "a")
    nome = nome.replace("é", "e")
    nome = nome.replace("ê", "e")
    nome = nome.replace("í", "i")
    nome = nome.replace("ó", "o")
    nome = nome.replace("ô", "o")
    nome = nome.replace("õ", "o")
    nome = nome.replace("ú", "u")
    nome = nome.replace("__", "_")
    return nome


def transformar_bronze_para_silver(
    input_path: str = "data/bronze/bronze_comercial.parquet",
    output_dir: str = "data/silver"
) -> Path:
    input_file = Path(input_path)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    if not input_file.exists():
        raise FileNotFoundError(f"Arquivo bronze não encontrado: {input_file}")

    print(f"Lendo Bronze: {input_file}")

    df = pd.read_parquet(input_file)

    print(f"Linhas recebidas da Bronze: {len(df)}")
    print(f"Colunas recebidas da Bronze: {len(df.columns)}")

    # Padronizar nomes das colunas
    df.columns = [padronizar_nome_coluna(col) for col in df.columns]

    # Remover linhas totalmente vazias
    df = df.dropna(how="all")

    # Remover espaços em branco de colunas texto
    colunas_texto = df.select_dtypes(include=["object"]).columns

    for coluna in colunas_texto:
        df[coluna] = df[coluna].astype(str).str.strip()
        df[coluna] = df[coluna].replace({"nan": None, "None": None, "": None})

    # Converter colunas de data, se existirem
    possiveis_colunas_data = [
        "data",
        "dt",
        "competencia",
        "data_competencia",
        "mes",
        "ano_mes"
    ]

    for coluna in df.columns:
        if coluna in possiveis_colunas_data or "data" in coluna or "dt_" in coluna:
            try:
                df[coluna] = pd.to_datetime(df[coluna], errors="ignore")
            except Exception:
                pass

    # Criar identificador técnico da linha
    df["id_linha_silver"] = range(1, len(df) + 1)

    # Atualizar camada
    df["camada"] = "silver"

    output_file = output_path / "silver_comercial.parquet"

    df.to_parquet(output_file, index=False)

    print(f"Arquivo silver salvo em: {output_file}")
    print(f"Total de linhas Silver: {len(df)}")
    print(f"Total de colunas Silver: {len(df.columns)}")

    return output_file