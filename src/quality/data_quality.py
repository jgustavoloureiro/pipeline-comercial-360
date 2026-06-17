from pathlib import Path
from datetime import datetime
import pandas as pd


def executar_validacoes_silver(
    input_path: str = "data/silver/silver_comercial.parquet",
    log_dir: str = "logs"
) -> bool:
    input_file = Path(input_path)
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)

    if not input_file.exists():
        raise FileNotFoundError(f"Arquivo Silver não encontrado: {input_file}")

    print(f"Lendo Silver para validação: {input_file}")

    df = pd.read_parquet(input_file)

    erros = []
    avisos = []

    # 1. Validar se a base está vazia
    if df.empty:
        erros.append("A base Silver está vazia.")

    # 2. Validar colunas obrigatórias
    colunas_obrigatorias = [
        "ano",
        "mes",
        "competencia",
        "regiao",
        "canal",
        "produto",
        "segmento",
        "leads",
        "oportunidades",
        "ganhos",
        "receita",
        "meta",
        "pipeline_aberto",
        "forecast_ponderado"
    ]

    for coluna in colunas_obrigatorias:
        if coluna not in df.columns:
            erros.append(f"Coluna obrigatória ausente: {coluna}")

    # Se faltou coluna obrigatória, não continua as validações específicas
    if erros:
        return _salvar_relatorio_qualidade(erros, avisos, log_path)

    # 3. Validar nulos em colunas essenciais
    colunas_nao_nulas = [
        "competencia",
        "regiao",
        "canal",
        "produto",
        "segmento"
    ]

    for coluna in colunas_nao_nulas:
        total_nulos = df[coluna].isna().sum()
        if total_nulos > 0:
            erros.append(f"Coluna {coluna} possui {total_nulos} valores nulos.")

    # 4. Validar valores negativos
    colunas_nao_negativas = [
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
        "velocidade_vendas"
    ]

    for coluna in colunas_nao_negativas:
        if coluna in df.columns:
            total_negativos = (df[coluna] < 0).sum()
            if total_negativos > 0:
                erros.append(f"Coluna {coluna} possui {total_negativos} valores negativos.")

    # 5. Validar mês entre 1 e 12
    meses_invalidos = (~df["mes"].between(1, 12)).sum()
    if meses_invalidos > 0:
        erros.append(f"Existem {meses_invalidos} registros com mês inválido.")

    # 6. Validar ano esperado
    anos_validos = [2025, 2026]
    anos_invalidos = (~df["ano"].isin(anos_validos)).sum()
    if anos_invalidos > 0:
        avisos.append(f"Existem {anos_invalidos} registros fora dos anos esperados: {anos_validos}.")

    # 7. Validar lógica do funil
    regras_funil = [
        ("mql", "leads"),
        ("sql", "mql"),
        ("oportunidades", "sql"),
        ("propostas", "oportunidades"),
        ("negociacao", "propostas"),
        ("ganhos", "negociacao")
    ]

    for menor, maior in regras_funil:
        total_invalidos = (df[menor] > df[maior]).sum()
        if total_invalidos > 0:
            avisos.append(
                f"Regra de funil: {menor} maior que {maior} em {total_invalidos} registros."
            )

    # 8. Validar duplicidade técnica
    if "id_linha_silver" in df.columns:
        duplicados = df["id_linha_silver"].duplicated().sum()
        if duplicados > 0:
            erros.append(f"Existem {duplicados} IDs técnicos duplicados na Silver.")

    return _salvar_relatorio_qualidade(erros, avisos, log_path)


def _salvar_relatorio_qualidade(erros, avisos, log_path: Path) -> bool:
    data_execucao = datetime.now().strftime("%Y%m%d_%H%M%S")
    arquivo_log = log_path / f"data_quality_silver_{data_execucao}.txt"

    status = "APROVADO" if not erros else "REPROVADO"

    linhas = []
    linhas.append("RELATÓRIO DE QUALIDADE - SILVER COMERCIAL")
    linhas.append("=" * 50)
    linhas.append(f"Data/Hora: {datetime.now()}")
    linhas.append(f"Status: {status}")
    linhas.append("")
    linhas.append("ERROS:")
    if erros:
        for erro in erros:
            linhas.append(f"- {erro}")
    else:
        linhas.append("- Nenhum erro encontrado.")
    linhas.append("")
    linhas.append("AVISOS:")
    if avisos:
        for aviso in avisos:
            linhas.append(f"- {aviso}")
    else:
        linhas.append("- Nenhum aviso encontrado.")

    conteudo = "\n".join(linhas)

    arquivo_log.write_text(conteudo, encoding="utf-8")

    print(conteudo)
    print(f"\nRelatório salvo em: {arquivo_log}")

    return not erros