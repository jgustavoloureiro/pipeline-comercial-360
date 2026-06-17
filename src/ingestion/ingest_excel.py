from pathlib import Path
from datetime import datetime
import pandas as pd


def ingest_excel_to_bronze(
    input_path: str,
    sheet_name: str,
    output_dir: str = "data/bronze"
) -> Path:
    input_file = Path(input_path)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    if not input_file.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {input_file}")

    print(f"Lendo arquivo: {input_file}")
    print(f"Lendo aba: {sheet_name}")

    df = pd.read_excel(
        input_file,
        sheet_name=sheet_name
    )

    df["arquivo_origem"] = input_file.name
    df["aba_origem"] = sheet_name
    df["data_carga"] = datetime.now()
    df["camada"] = "bronze"

    output_file = output_path / "bronze_comercial.parquet"

    df.to_parquet(output_file, index=False)

    print(f"Arquivo bronze salvo em: {output_file}")
    print(f"Total de linhas: {len(df)}")
    print(f"Total de colunas: {len(df.columns)}")

    return output_file
    