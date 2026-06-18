import duckdb


def consultar_modelo_dimensional():
    con = duckdb.connect("database/comercial_analytics.duckdb")

    print("=" * 100)
    print("Consulta dimensional — Receita e Pipeline por mês, produto, região e canal")
    print("=" * 100)

    consulta = """
        SELECT
            t.competencia,
            t.rotulo,
            p.produto,
            r.regiao,
            c.canal,
            SUM(f.receita) AS receita,
            SUM(f.meta) AS meta,
            SUM(f.pipeline_aberto) AS pipeline_aberto,
            SUM(f.forecast_ponderado) AS forecast_ponderado,
            SUM(f.ganhos) AS ganhos,
            SUM(f.oportunidades) AS oportunidades,
            ROUND(SUM(f.receita) / NULLIF(SUM(f.meta), 0) * 100, 2) AS atingimento_meta_pct,
            ROUND(SUM(f.ganhos) / NULLIF(SUM(f.oportunidades), 0) * 100, 2) AS win_rate_pct
        FROM vw_fato_comercial f
        INNER JOIN vw_dim_tempo t
            ON f.sk_tempo = t.sk_tempo
        INNER JOIN vw_dim_produto p
            ON f.sk_produto = p.sk_produto
        INNER JOIN vw_dim_regiao r
            ON f.sk_regiao = r.sk_regiao
        INNER JOIN vw_dim_canal c
            ON f.sk_canal = c.sk_canal
        GROUP BY
            t.competencia,
            t.rotulo,
            p.produto,
            r.regiao,
            c.canal
        ORDER BY
            t.competencia,
            receita DESC
        LIMIT 20
    """

    resultado = con.execute(consulta).df()
    print(resultado)

    print("\n")
    print("=" * 100)
    print("Top 10 combinações por receita")
    print("=" * 100)

    top_receita = """
        SELECT
            p.produto,
            r.regiao,
            c.canal,
            s.segmento,
            ROUND(SUM(f.receita), 2) AS receita,
            ROUND(SUM(f.pipeline_aberto), 2) AS pipeline_aberto,
            ROUND(SUM(f.forecast_ponderado), 2) AS forecast_ponderado,
            SUM(f.ganhos) AS ganhos
        FROM vw_fato_comercial f
        INNER JOIN vw_dim_produto p
            ON f.sk_produto = p.sk_produto
        INNER JOIN vw_dim_regiao r
            ON f.sk_regiao = r.sk_regiao
        INNER JOIN vw_dim_canal c
            ON f.sk_canal = c.sk_canal
        INNER JOIN vw_dim_segmento s
            ON f.sk_segmento = s.sk_segmento
        GROUP BY
            p.produto,
            r.regiao,
            c.canal,
            s.segmento
        ORDER BY
            receita DESC
        LIMIT 10
    """

    resultado_top = con.execute(top_receita).df()
    print(resultado_top)

    con.close()


if __name__ == "__main__":
    consultar_modelo_dimensional()