from pathlib import Path
import pandas as pd


def construir_gold_dimensional(
    input_path: str = "data/silver/silver_comercial.parquet",
    output_dir: str = "data/gold"
) -> dict:
    input_file = Path(input_path)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    if not input_file.exists():
        raise FileNotFoundError(f"Arquivo Silver não encontrado: {input_file}")

    print(f"Lendo Silver para construir Gold Dimensional: {input_file}")

    df = pd.read_parquet(input_file)

    # ==========================================================
    # DIMENSÃO TEMPO
    # ==========================================================
    dim_tempo = (
        df[[
            "ano",
            "mes",
            "competencia",
            "rotulo",
            "trimestre",
            "semestre",
            "ano_periodo"
        ]]
        .drop_duplicates()
        .sort_values(["ano", "mes"])
        .reset_index(drop=True)
    )

    dim_tempo["sk_tempo"] = range(1, len(dim_tempo) + 1)

    dim_tempo = dim_tempo[[
        "sk_tempo",
        "ano",
        "mes",
        "competencia",
        "rotulo",
        "trimestre",
        "semestre",
        "ano_periodo"
    ]]

    # ==========================================================
    # DIMENSÃO PRODUTO
    # ==========================================================
    dim_produto = (
        df[["produto"]]
        .drop_duplicates()
        .sort_values("produto")
        .reset_index(drop=True)
    )

    dim_produto["sk_produto"] = range(1, len(dim_produto) + 1)

    dim_produto = dim_produto[[
        "sk_produto",
        "produto"
    ]]

    # ==========================================================
    # DIMENSÃO REGIÃO
    # ==========================================================
    dim_regiao = (
        df[["regiao"]]
        .drop_duplicates()
        .sort_values("regiao")
        .reset_index(drop=True)
    )

    dim_regiao["sk_regiao"] = range(1, len(dim_regiao) + 1)

    dim_regiao = dim_regiao[[
        "sk_regiao",
        "regiao"
    ]]

    # ==========================================================
    # DIMENSÃO CANAL
    # ==========================================================
    dim_canal = (
        df[["canal"]]
        .drop_duplicates()
        .sort_values("canal")
        .reset_index(drop=True)
    )

    dim_canal["sk_canal"] = range(1, len(dim_canal) + 1)

    dim_canal = dim_canal[[
        "sk_canal",
        "canal"
    ]]

    # ==========================================================
    # DIMENSÃO SEGMENTO
    # ==========================================================
    dim_segmento = (
        df[["segmento"]]
        .drop_duplicates()
        .sort_values("segmento")
        .reset_index(drop=True)
    )

    dim_segmento["sk_segmento"] = range(1, len(dim_segmento) + 1)

    dim_segmento = dim_segmento[[
        "sk_segmento",
        "segmento"
    ]]

    # ==========================================================
    # FATO COMERCIAL
    # ==========================================================
    fato = df.copy()

    fato = fato.merge(
        dim_tempo,
        on=[
            "ano",
            "mes",
            "competencia",
            "rotulo",
            "trimestre",
            "semestre",
            "ano_periodo"
        ],
        how="left"
    )

    fato = fato.merge(dim_produto, on="produto", how="left")
    fato = fato.merge(dim_regiao, on="regiao", how="left")
    fato = fato.merge(dim_canal, on="canal", how="left")
    fato = fato.merge(dim_segmento, on="segmento", how="left")

    fato_comercial = fato[[
        "id_linha_silver",
        "sk_tempo",
        "sk_produto",
        "sk_regiao",
        "sk_canal",
        "sk_segmento",
        "leads",
        "mql",
        "sql",
        "oportunidades",
        "propostas",
        "negociacao",
        "ganhos",
        "perdidos",
        "receita",
        "meta",
        "pipeline_aberto",
        "forecast_ponderado",
        "ticket_medio",
        "cac",
        "ciclo_medio_dias",
        "win_rate",
        "conversao_lead_venda",
        "velocidade_vendas",
        "arquivo_origem",
        "aba_origem",
        "data_carga"
    ]].copy()

    fato_comercial = fato_comercial.rename(
        columns={
            "id_linha_silver": "id_fato_comercial"
        }
    )

    # ==========================================================
    # SALVAR ARQUIVOS
    # ==========================================================
    arquivos = {
        "dim_tempo": output_path / "dim_tempo.parquet",
        "dim_produto": output_path / "dim_produto.parquet",
        "dim_regiao": output_path / "dim_regiao.parquet",
        "dim_canal": output_path / "dim_canal.parquet",
        "dim_segmento": output_path / "dim_segmento.parquet",
        "fato_comercial": output_path / "fato_comercial.parquet"
    }

    dim_tempo.to_parquet(arquivos["dim_tempo"], index=False)
    dim_produto.to_parquet(arquivos["dim_produto"], index=False)
    dim_regiao.to_parquet(arquivos["dim_regiao"], index=False)
    dim_canal.to_parquet(arquivos["dim_canal"], index=False)
    dim_segmento.to_parquet(arquivos["dim_segmento"], index=False)
    fato_comercial.to_parquet(arquivos["fato_comercial"], index=False)

    print("Gold Dimensional criada com sucesso:")
    for nome, caminho in arquivos.items():
        print(f"- {nome}: {caminho}")

    print("")
    print("Resumo dimensional:")
    print(f"- dim_tempo: {len(dim_tempo)} linhas")
    print(f"- dim_produto: {len(dim_produto)} linhas")
    print(f"- dim_regiao: {len(dim_regiao)} linhas")
    print(f"- dim_canal: {len(dim_canal)} linhas")
    print(f"- dim_segmento: {len(dim_segmento)} linhas")
    print(f"- fato_comercial: {len(fato_comercial)} linhas")

    return arquivos