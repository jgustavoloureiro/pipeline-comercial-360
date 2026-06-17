from pathlib import Path
import pandas as pd


def construir_gold_comercial(
    input_path: str = "data/silver/silver_comercial.parquet",
    output_dir: str = "data/gold"
) -> dict:
    input_file = Path(input_path)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    if not input_file.exists():
        raise FileNotFoundError(f"Arquivo Silver não encontrado: {input_file}")

    print(f"Lendo Silver para construir Gold: {input_file}")

    df = pd.read_parquet(input_file)

    # GOLD 1: KPIs comerciais por período
    gold_kpis = (
        df.groupby(["ano", "mes", "competencia", "rotulo"], as_index=False)
        .agg(
            leads=("leads", "sum"),
            mql=("mql", "sum"),
            sql=("sql", "sum"),
            oportunidades=("oportunidades", "sum"),
            propostas=("propostas", "sum"),
            negociacao=("negociacao", "sum"),
            ganhos=("ganhos", "sum"),
            perdidos=("perdidos", "sum"),
            receita=("receita", "sum"),
            meta=("meta", "sum"),
            pipeline_aberto=("pipeline_aberto", "sum"),
            forecast_ponderado=("forecast_ponderado", "sum"),
            ticket_medio=("ticket_medio", "mean"),
            cac=("cac", "mean"),
            ciclo_medio_dias=("ciclo_medio_dias", "mean"),
            velocidade_vendas=("velocidade_vendas", "sum")
        )
    )

    gold_kpis["atingimento_meta"] = gold_kpis["receita"] / gold_kpis["meta"]
    gold_kpis["win_rate"] = gold_kpis["ganhos"] / gold_kpis["oportunidades"]
    gold_kpis["conversao_lead_venda"] = gold_kpis["ganhos"] / gold_kpis["leads"]

    gold_kpis_file = output_path / "gold_kpis_comerciais.parquet"
    gold_kpis.to_parquet(gold_kpis_file, index=False)

    # GOLD 2: Funil comercial consolidado
    etapas_funil = [
        ("Leads", "leads"),
        ("MQL", "mql"),
        ("SQL", "sql"),
        ("Oportunidades", "oportunidades"),
        ("Propostas", "propostas"),
        ("Negociação", "negociacao"),
        ("Ganhos", "ganhos")
    ]

    linhas_funil = []

    for ordem, (etapa, coluna) in enumerate(etapas_funil, start=1):
        linhas_funil.append(
            {
                "ordem": ordem,
                "etapa": etapa,
                "quantidade": df[coluna].sum()
            }
        )

    gold_funil = pd.DataFrame(linhas_funil)

    total_leads = gold_funil.loc[
        gold_funil["etapa"] == "Leads",
        "quantidade"
    ].iloc[0]

    gold_funil["conversao_sobre_leads"] = (
        gold_funil["quantidade"] / total_leads
    )

    gold_funil_file = output_path / "gold_funil_comercial.parquet"
    gold_funil.to_parquet(gold_funil_file, index=False)

    # GOLD 3: Pipeline por produto
    gold_pipeline_produto = (
        df.groupby(["produto"], as_index=False)
        .agg(
            pipeline_aberto=("pipeline_aberto", "sum"),
            forecast_ponderado=("forecast_ponderado", "sum"),
            receita=("receita", "sum"),
            oportunidades=("oportunidades", "sum"),
            ganhos=("ganhos", "sum")
        )
        .sort_values("pipeline_aberto", ascending=False)
    )

    gold_pipeline_produto["conversao_pipeline_forecast"] = (
        gold_pipeline_produto["forecast_ponderado"]
        / gold_pipeline_produto["pipeline_aberto"]
    )

    gold_pipeline_file = output_path / "gold_pipeline_produto.parquet"
    gold_pipeline_produto.to_parquet(gold_pipeline_file, index=False)

    print("Camada Gold criada com sucesso:")
    print(f"- {gold_kpis_file}")
    print(f"- {gold_funil_file}")
    print(f"- {gold_pipeline_file}")

    return {
        "gold_kpis": gold_kpis_file,
        "gold_funil": gold_funil_file,
        "gold_pipeline_produto": gold_pipeline_file
    }