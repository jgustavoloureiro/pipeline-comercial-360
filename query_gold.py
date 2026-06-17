import duckdb


def executar_consultas_gold():
    con = duckdb.connect()

    print("=" * 80)
    print("Consulta 1 - Receita, meta e atingimento por mês")
    print("=" * 80)

    consulta_kpis = """
        SELECT
            competencia,
            rotulo,
            ROUND(receita, 2) AS receita,
            ROUND(meta, 2) AS meta,
            ROUND(atingimento_meta * 100, 2) AS atingimento_meta_pct,
            ROUND(win_rate * 100, 2) AS win_rate_pct
        FROM 'data/gold/gold_kpis_comerciais.parquet'
        ORDER BY
            ano,
            mes
    """

    resultado_kpis = con.execute(consulta_kpis).df()
    print(resultado_kpis)

    print("\n")
    print("=" * 80)
    print("Consulta 2 - Funil comercial consolidado")
    print("=" * 80)

    consulta_funil = """
        SELECT
            ordem,
            etapa,
            quantidade,
            ROUND(conversao_sobre_leads * 100, 2) AS conversao_sobre_leads_pct
        FROM 'data/gold/gold_funil_comercial.parquet'
        ORDER BY ordem
    """

    resultado_funil = con.execute(consulta_funil).df()
    print(resultado_funil)

    print("\n")
    print("=" * 80)
    print("Consulta 3 - Top produtos por pipeline aberto")
    print("=" * 80)

    consulta_pipeline = """
        SELECT
            produto,
            ROUND(pipeline_aberto, 2) AS pipeline_aberto,
            ROUND(forecast_ponderado, 2) AS forecast_ponderado,
            ROUND(receita, 2) AS receita,
            oportunidades,
            ganhos,
            ROUND(conversao_pipeline_forecast * 100, 2) AS conversao_pipeline_forecast_pct
        FROM 'data/gold/gold_pipeline_produto.parquet'
        ORDER BY pipeline_aberto DESC
    """

    resultado_pipeline = con.execute(consulta_pipeline).df()
    print(resultado_pipeline)

    con.close()


if __name__ == "__main__":
    executar_consultas_gold()