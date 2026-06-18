from src.ingestion.ingest_excel import ingest_excel_to_bronze
from src.transformation.transform_silver import transformar_bronze_para_silver
from src.quality.data_quality import executar_validacoes_silver
from src.transformation.build_gold import construir_gold_comercial
from src.transformation.build_dimensional_gold import construir_gold_dimensional


def main():
    print("Iniciando pipeline de dados comercial 360")

    bronze_file = ingest_excel_to_bronze(
        input_path="data/raw/base_comercial_funil_360.xlsx",
        sheet_name="Base_Comercial",
        output_dir="data/bronze"
    )

    silver_file = transformar_bronze_para_silver(
        input_path=str(bronze_file),
        output_dir="data/silver"
    )

    qualidade_aprovada = executar_validacoes_silver(
        input_path=str(silver_file),
        log_dir="logs"
    )

    if not qualidade_aprovada:
        print("Pipeline interrompido. Qualidade reprovada.")
        return

    gold_files = construir_gold_comercial(
        input_path=str(silver_file),
        output_dir="data/gold"
    )

    gold_dimensional_files = construir_gold_dimensional(
        input_path=str(silver_file),
        output_dir="data/gold"
    )

    print("Pipeline finalizado com sucesso.")
    print(f"Bronze: {bronze_file}")
    print(f"Silver: {silver_file}")

    print("Gold Analítica:")
    for nome, caminho in gold_files.items():
        print(f"- {nome}: {caminho}")

    print("Gold Dimensional:")
    for nome, caminho in gold_dimensional_files.items():
        print(f"- {nome}: {caminho}")


if __name__ == "__main__":
    main()