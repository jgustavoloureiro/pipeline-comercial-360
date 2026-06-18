# Pipeline Comercial 360 — Engenharia de Dados

Projeto de Engenharia de Dados desenvolvido em Python para estruturar um pipeline analítico a partir de uma base comercial em Excel.

O objetivo é demonstrar um fluxo ponta a ponta de dados, saindo de uma fonte bruta, passando por camadas de tratamento, validação e modelagem, até a disponibilização dos dados para consumo analítico via SQL.

---

## Visão Geral

O projeto segue uma arquitetura em camadas:

```text
Excel Raw
   ↓
Bronze
   ↓
Silver
   ↓
Data Quality
   ↓
Gold Analítica
   ↓
Gold Dimensional
   ↓
DuckDB Analytics
   ↓
SQL Views
```

Essa estrutura simula práticas utilizadas em ambientes de Engenharia de Dados, Analytics Engineering e Business Intelligence.

---

## Objetivo do Projeto

Construir um pipeline de dados capaz de:

* Ler uma base comercial em Excel
* Criar uma camada Bronze em Parquet
* Padronizar e tratar os dados na camada Silver
* Executar validações de qualidade
* Criar tabelas Gold analíticas
* Criar um modelo dimensional com fatos e dimensões
* Disponibilizar os dados em um banco DuckDB
* Consultar os dados por meio de SQL

---

## Tecnologias Utilizadas

* Python
* Pandas
* OpenPyXL
* PyArrow
* Parquet
* DuckDB
* SQL
* Git
* GitHub

---

## Estrutura do Projeto

```text
pipeline-comercial-360/
│
├── data/
│   ├── raw/
│   │   └── base_comercial_funil_360.xlsx
│   │
│   ├── bronze/
│   │   └── bronze_comercial.parquet
│   │
│   ├── silver/
│   │   └── silver_comercial.parquet
│   │
│   └── gold/
│       ├── gold_kpis_comerciais.parquet
│       ├── gold_funil_comercial.parquet
│       ├── gold_pipeline_produto.parquet
│       ├── dim_tempo.parquet
│       ├── dim_produto.parquet
│       ├── dim_regiao.parquet
│       ├── dim_canal.parquet
│       ├── dim_segmento.parquet
│       └── fato_comercial.parquet
│
├── database/
│   └── comercial_analytics.duckdb
│
├── logs/
│
├── src/
│   ├── ingestion/
│   │   └── ingest_excel.py
│   │
│   ├── transformation/
│   │   ├── transform_silver.py
│   │   ├── build_gold.py
│   │   └── build_dimensional_gold.py
│   │
│   └── quality/
│       └── data_quality.py
│
├── check_excel.py
├── check_silver.py
├── check_gold.py
├── create_database.py
├── query_gold.py
├── query_database.py
├── query_dimensional.py
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Arquitetura em Camadas

### Raw

Camada de entrada contendo o arquivo original em Excel.

```text
data/raw/base_comercial_funil_360.xlsx
```

Essa camada representa a fonte original dos dados, antes de qualquer transformação.

---

### Bronze

Camada de ingestão dos dados.

Nesta etapa, a base Excel é lida e convertida para Parquet, mantendo a estrutura próxima da origem e adicionando colunas técnicas de rastreabilidade.

Colunas técnicas adicionadas:

* arquivo_origem
* aba_origem
* data_carga
* camada

Arquivo gerado:

```text
data/bronze/bronze_comercial.parquet
```

---

### Silver

Camada de tratamento e padronização.

Nesta etapa são aplicadas regras como:

* Padronização dos nomes das colunas
* Remoção de espaços em branco
* Tratamento de valores nulos
* Conversão e organização de tipos de dados
* Criação de identificador técnico
* Preparação da base para uso analítico

Arquivo gerado:

```text
data/silver/silver_comercial.parquet
```

---

## Data Quality

Antes da construção da camada Gold, o pipeline executa validações de qualidade sobre a camada Silver.

Validações implementadas:

* Verificação se a base está vazia
* Verificação de colunas obrigatórias
* Validação de nulos em campos essenciais
* Validação de valores negativos em métricas comerciais
* Validação de mês entre 1 e 12
* Validação de anos esperados
* Validação lógica das etapas do funil
* Verificação de duplicidade técnica

Os relatórios são salvos em:

```text
logs/
```

Quando a qualidade é aprovada, o pipeline segue para a camada Gold.

---

## Gold Analítica

A camada Gold Analítica consolida os dados em tabelas prontas para consumo direto por dashboards, análises e consultas SQL.

Tabelas criadas:

```text
gold_kpis_comerciais.parquet
gold_funil_comercial.parquet
gold_pipeline_produto.parquet
```

### gold_kpis_comerciais

Tabela consolidada por competência, contendo indicadores como:

* Leads
* MQL
* SQL
* Oportunidades
* Propostas
* Negociação
* Ganhos
* Perdidos
* Receita
* Meta
* Pipeline aberto
* Forecast ponderado
* Atingimento da meta
* Win rate
* Conversão lead-venda

### gold_funil_comercial

Tabela consolidada das etapas do funil comercial:

* Leads
* MQL
* SQL
* Oportunidades
* Propostas
* Negociação
* Ganhos

### gold_pipeline_produto

Tabela consolidada de pipeline por produto, com métricas como:

* Pipeline aberto
* Forecast ponderado
* Receita
* Oportunidades
* Ganhos
* Conversão pipeline-forecast

---

## Gold Dimensional

Além das tabelas Gold analíticas, o projeto possui uma camada Gold Dimensional estruturada em modelo estrela.

Essa modelagem separa as entidades descritivas em dimensões e mantém as métricas na tabela fato.

Dimensões criadas:

```text
dim_tempo.parquet
dim_produto.parquet
dim_regiao.parquet
dim_canal.parquet
dim_segmento.parquet
```

Tabela fato criada:

```text
fato_comercial.parquet
```

### Modelo Estrela

```text
dim_tempo
dim_produto
dim_regiao
dim_canal
dim_segmento
        ↓
  fato_comercial
```

Essa estrutura permite análises por diferentes perspectivas, como:

* Tempo
* Produto
* Região
* Canal
* Segmento

A modelagem dimensional facilita o consumo dos dados em ferramentas de BI, Data Warehouse e consultas SQL analíticas.

---

## DuckDB Analytics

Após a construção das camadas Gold, o projeto cria um banco analítico local utilizando DuckDB.

Arquivo gerado:

```text
database/comercial_analytics.duckdb
```

Views criadas sobre a Gold Analítica:

```text
vw_gold_kpis_comerciais
vw_gold_funil_comercial
vw_gold_pipeline_produto
```

Views criadas sobre a Gold Dimensional:

```text
vw_dim_tempo
vw_dim_produto
vw_dim_regiao
vw_dim_canal
vw_dim_segmento
vw_fato_comercial
```

Essas views permitem consultar os dados tratados e modelados diretamente via SQL.

---

## Como Executar o Projeto

### 1. Criar ambiente virtual

```bash
python -m venv .venv
```

### 2. Ativar ambiente virtual

No Windows:

```bash
.venv\Scripts\activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Executar pipeline principal

```bash
python main.py
```

Esse comando executa:

```text
Raw → Bronze
Bronze → Silver
Validação de qualidade
Gold Analítica
Gold Dimensional
```

### 5. Criar ou atualizar banco DuckDB

```bash
python create_database.py
```

### 6. Consultar views analíticas

```bash
python query_database.py
```

### 7. Consultar modelo dimensional

```bash
python query_dimensional.py
```

---

## Consultas Auxiliares

O projeto também possui scripts de conferência para validar as camadas criadas.

### Verificar abas da base Excel

```bash
python check_excel.py
```

### Verificar camada Silver

```bash
python check_silver.py
```

### Verificar camada Gold

```bash
python check_gold.py
```

### Consultar arquivos Gold diretamente com DuckDB

```bash
python query_gold.py
```

---

## Exemplos de Consultas SQL

### Receita, meta e atingimento por mês

```sql
SELECT
    competencia,
    rotulo,
    receita,
    meta,
    atingimento_meta
FROM vw_gold_kpis_comerciais
ORDER BY ano, mes;
```

---

### Pipeline por produto

```sql
SELECT
    produto,
    pipeline_aberto,
    forecast_ponderado,
    receita
FROM vw_gold_pipeline_produto
ORDER BY pipeline_aberto DESC;
```

---

### Funil comercial consolidado

```sql
SELECT
    ordem,
    etapa,
    quantidade,
    conversao_sobre_leads
FROM vw_gold_funil_comercial
ORDER BY ordem;
```

---

### Consulta dimensional com fato e dimensões

```sql
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
    ROUND(SUM(f.receita) / NULLIF(SUM(f.meta), 0) * 100, 2) AS atingimento_meta_pct
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
    receita DESC;
```

---

## Resultado Esperado

Ao executar o pipeline principal, os seguintes arquivos são gerados:

```text
data/bronze/bronze_comercial.parquet
data/silver/silver_comercial.parquet
data/gold/gold_kpis_comerciais.parquet
data/gold/gold_funil_comercial.parquet
data/gold/gold_pipeline_produto.parquet
data/gold/dim_tempo.parquet
data/gold/dim_produto.parquet
data/gold/dim_regiao.parquet
data/gold/dim_canal.parquet
data/gold/dim_segmento.parquet
data/gold/fato_comercial.parquet
```

Após executar o script de banco:

```text
database/comercial_analytics.duckdb
```

---

## Principais Competências Demonstradas

* Engenharia de Dados com Python
* Ingestão de dados a partir de Excel
* Arquitetura em camadas
* Criação de camadas Bronze, Silver e Gold
* Uso de arquivos Parquet
* Tratamento e padronização de dados
* Validação de qualidade de dados
* Modelagem analítica
* Modelagem dimensional
* Construção de modelo estrela
* Criação de tabela fato e dimensões
* Uso de DuckDB como banco analítico local
* Criação de views SQL
* Consultas analíticas com SQL
* Organização de projeto para GitHub
* Versionamento com Git

---

## Próximas Evoluções

Possíveis melhorias futuras para o projeto:

* Implementação com dbt
* Criação de testes automatizados com dbt tests
* Orquestração com Prefect ou Airflow
* Containerização com Docker
* Execução automatizada com GitHub Actions
* Integração com Power BI
* Simulação em ambiente cloud com Azure, Fabric ou AWS

---

## Autor

Projeto desenvolvido por **José Gustavo Loureiro Campos Silva** como parte de um portfólio focado em Engenharia de Dados, Analytics Engineering e Business Intelligence.
