# Pipeline Comercial 360 — Engenharia de Dados

Projeto de Engenharia de Dados desenvolvido em Python para estruturar um pipeline analítico a partir de uma base comercial em Excel.

O objetivo é simular uma arquitetura moderna em camadas, transformando dados brutos em tabelas analíticas prontas para consumo em dashboards, consultas SQL e análises de negócio.

---

## Visão Geral

Este projeto realiza o fluxo completo:

```text
Excel Raw
   ↓
Bronze
   ↓
Silver
   ↓
Data Quality
   ↓
Gold
   ↓
DuckDB Analytics
   ↓
SQL Views
```

A proposta é demonstrar práticas fundamentais de Engenharia de Dados, incluindo ingestão, padronização, validação, modelagem analítica e disponibilização dos dados para consumo.

---

## Tecnologias Utilizadas

* Python
* Pandas
* OpenPyXL
* PyArrow
* Parquet
* DuckDB
* SQL

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
│       └── gold_pipeline_produto.parquet
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
│   │   └── build_gold.py
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
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Camadas do Pipeline

### Raw

Camada de entrada contendo o arquivo original em Excel.

```text
data/raw/base_comercial_funil_360.xlsx
```

Essa camada representa a fonte original dos dados antes de qualquer tratamento.

---

### Bronze

Camada de ingestão, onde os dados são lidos da origem e salvos em formato Parquet, mantendo a estrutura próxima da fonte original.

Também são adicionadas colunas técnicas, como:

* arquivo de origem
* aba de origem
* data de carga
* camada

Arquivo gerado:

```text
data/bronze/bronze_comercial.parquet
```

---

### Silver

Camada de tratamento e padronização.

Nesta etapa são aplicadas regras como:

* padronização dos nomes das colunas
* remoção de espaços em branco
* tratamento de valores nulos
* criação de identificador técnico
* organização da base para uso analítico

Arquivo gerado:

```text
data/silver/silver_comercial.parquet
```

---

### Data Quality

Camada de validação da qualidade dos dados.

Foram implementadas validações como:

* base não pode estar vazia
* colunas obrigatórias precisam existir
* campos essenciais não podem ser nulos
* métricas comerciais não podem ter valores negativos
* mês precisa estar entre 1 e 12
* validação lógica das etapas do funil
* verificação de duplicidade técnica

Os relatórios de qualidade são salvos em:

```text
logs/
```

---

### Gold

Camada analítica modelada para consumo.

Foram criadas três tabelas principais:

```text
gold_kpis_comerciais.parquet
gold_funil_comercial.parquet
gold_pipeline_produto.parquet
```

Essas tabelas consolidam os dados para análises de:

* receita
* meta
* atingimento da meta
* win rate
* conversão do funil
* pipeline por produto
* forecast ponderado

---

## DuckDB Analytics

Após a criação da camada Gold, o projeto cria um banco analítico local usando DuckDB.

Arquivo gerado:

```text
database/comercial_analytics.duckdb
```

Views disponíveis:

```text
vw_gold_kpis_comerciais
vw_gold_funil_comercial
vw_gold_pipeline_produto
```

Essas views permitem consultar a camada Gold usando SQL.

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
Ingestão Raw → Bronze
Transformação Bronze → Silver
Validação de qualidade
Construção da camada Gold
```

### 5. Criar banco DuckDB

```bash
python create_database.py
```

### 6. Consultar o banco analítico

```bash
python query_database.py
```

---

## Consultas Auxiliares

O projeto também possui arquivos auxiliares para conferência das camadas.

### Verificar abas do Excel

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

Consulta de receita, meta e atingimento por mês:

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

Consulta de pipeline por produto:

```sql
SELECT
    produto,
    pipeline_aberto,
    forecast_ponderado,
    receita
FROM vw_gold_pipeline_produto
ORDER BY pipeline_aberto DESC;
```

Consulta do funil comercial consolidado:

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

## Resultado Esperado

Ao executar o pipeline principal, espera-se a geração dos seguintes arquivos:

```text
data/bronze/bronze_comercial.parquet
data/silver/silver_comercial.parquet
data/gold/gold_kpis_comerciais.parquet
data/gold/gold_funil_comercial.parquet
data/gold/gold_pipeline_produto.parquet
```

Após executar o script de criação do banco, também será gerado:

```text
database/comercial_analytics.duckdb
```

---

## Objetivo do Projeto

Este projeto foi desenvolvido com foco em portfólio de Engenharia de Dados, demonstrando a construção de um pipeline analítico ponta a ponta.

A solução cobre desde a ingestão de uma base Excel até a disponibilização dos dados em uma camada Gold consultável via SQL.

---

## Principais Competências Demonstradas

* Ingestão de dados com Python
* Manipulação de arquivos Excel
* Criação de arquitetura em camadas
* Uso de arquivos Parquet
* Tratamento e padronização de dados
* Validação de qualidade
* Modelagem de dados analíticos
* Consultas SQL com DuckDB
* Criação de banco analítico local
* Organização de projeto para GitHub
* Preparação de dados para dashboards e análises

---

## Autor

Projeto desenvolvido por José Gustavo Loureiro Campos Silva como parte de um portfólio focado em Engenharia de Dados, Analytics Engineering e Business Intelligence.
