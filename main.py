import duckdb


def consultar_banco_analytics():
    con = duckdb.connect("database/comercial_analytics.duckdb")

    print("=" * 80)
    print("Views disponíveis no banco")
    print("=" * 80)

    views = con.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'main'
        ORDER BY table_name
    """).df()

    print(views)

    print("\n")
    print("=" * 80)
    print("Receita, meta e atingimento por mês")
    print("=" * 80)

    resultado_kpis = con.execute("""
        SELECT
            competencia,
            rotulo,
            ROUND(receita, 2) AS receita,
            ROUND(meta, 2) AS meta,
            ROUND(atingimento_meta * 100, 2) AS atingimento_meta_pct,
            ROUND(win_rate * 100, 2) AS win_rate_pct
        FROM vw_gold_kpis_comerciais
        ORDER BY ano, mes
    """).df()

    print(resultado_kpis)

    print("\n")
    print("=" * 80)
    print("Top produtos por pipeline")
    print("=" * 80)

    resultado_pipeline = con.execute("""
        SELECT
            produto,
            ROUND(pipeline_aberto, 2) AS pipeline_aberto,
            ROUND(forecast_ponderado, 2) AS forecast_ponderado,
            ROUND(receita, 2) AS receita,
            oportunidades,
            ganhos,
            ROUND(conversao_pipeline_forecast * 100, 2) AS conversao_pipeline_forecast_pct
        FROM vw_gold_pipeline_produto
        ORDER BY pipeline_aberto DESC
    """).df()

    print(resultado_pipeline)

    con.close()


if __name__ == "__main__":
    consultar_banco_analytics()