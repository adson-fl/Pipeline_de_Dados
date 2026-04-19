# Pipeline de Dados com Apache Airflow (Arquitetura Medalhão)

## Descrição
Este projeto implementa um pipeline de dados utilizando Python, PostgreSQL e Apache Airflow, seguindo a arquitetura medalhão:

RAW: ingestão de dados via API
SILVER: transformação e padronização
GOLD: agregação para análise

O pipeline realiza extração de dados de usuários e posts, transforma os dados e gera métricas agregadas por usuário.

---

## Tecnologias Utilizadas
. Python
. PostgreSQL
. Apache Airflow
. Pandas
. SQLAlchemy

---

## Estrutura do Projeto
teste-tecnico-dados/ 
├── README.md 
├── requirements.txt 
├── .gitignore 
├── dags/ 
│ ├── dag_raw_extract.py 
│ ├── dag_silver_transform.py 
│ └── dag_gold_aggregate.py 
├── src/ 
│ ├── __init__.py 
│ └── extract_api.py 
└── scripts/ 
├── 01_create_raw_tables.sql 
├── 02_create_silver_tables.sql 
├── 03_create_gold_tables.sql 
├── transformations/ 
│ ├── raw_to_silver_usuarios.sql 
│ ├── raw_to_silver_posts.sql 
│ └── silver_to_gold_metricas.sql 
└── data_quality/ 
│ ├── check_usuarios_email.sql 
│ ├── check_posts_duplicados.sql 
│ └── check_contagem_registros.sql

---

# Configuração do Ambiente

## 1. Criar ambiente e instalar dependências

. pip install -r requirements.txt

---

## 2. Criar banco de dados

*Criar manualmente no PostgreSQL:*
. Database: teste_dados
. User: etl_user

---

## 3. Criar tabelas 

*execute os scripts SQL:*

. scripts/01_create_raw_tables.sql
. scripts/02_create_silver_tables.sql
. scripts/03_create_gold_tables.sql

---

## 4. Execução do Pipeline (modo manual)

Como o Airflow não é obrigatório para execução no teste, o pipeline pode ser executado diretamente via Python:

from dags.dag_raw_extract import load_usuarios, load_posts
from dags.dag_silver_transform import transform_usuarios, transform_posts
from dags.dag_gold_aggregate import create_metricas_usuario

load_usuarios()
load_posts()

transform_usuarios()
transform_posts()

create_metricas_usuario()

---

### Execução via Airflow

*Caso deseje executar via Airflow:*

airflow db init
airflow webserver --port 8080 
airflow scheduler

DAGs disponíveis: 
. etl_raw_extract
. etl_silver_transform
. etl_gold_aggregate

---

## Data Quality

Foram implementadas validações de qualidade de dados:

. Contagem entre camadas (RAW -> SILVER -> GOLD)
. Verificação de duplicidade de posts
. Validação de emails inválidos (sem '@')

Scripts disponíveis em:
scripts/data_quality/

---
## Observações 

. O pipeline pode ser executado manualmente para validação rápida.
. As DAGs foram estruturadas para execução independente.
. As validações de qualidade garantem integridade dos dados ao longo das camadas

## Objetivo do Projeto 

Este projeto foi desenvolvido como parte de um teste técnico para avaliação de habilidades em engenharia de dados.