# Pipeline de Dados com Apache Airflow (Arquitetura Medalhão)

## Descrição
Este projeto implementa um pipeline de dados utilizando Python, PostgreSQL e Apache Airflow, seguindo a arquitetura medalhão:

- **RAW**: ingestão de dados via API ([JSONPlaceholder](https://jsonplaceholder.typicode.com): `/users` e `/posts`)
- **SILVER**: transformação e padronização
- **GOLD**: agregação para análise

O pipeline realiza extração de dados de usuários e posts, transforma os dados e gera métricas agregadas por usuário.

---

## Tecnologias Utilizadas
- Python 3.9
- PostgreSQL
- Apache Airflow 2.7.3
- Pandas
- SQLAlchemy
- Requests
- python-dotenv

---

## Estrutura do Projeto
```
teste-tecnico-dados/
├── README.md
├── requirements.txt
├── .gitignore
├── .env.example
├── dags/
│   ├── dag_raw_extract.py
│   ├── dag_silver_transform.py
│   └── dag_gold_aggregate.py
├── src/
│   ├── __init__.py
│   ├── config.py
│   └── extract_api.py
└── scripts/
    ├── 01_create_raw_tables.sql
    ├── 02_create_silver_tables.sql
    ├── 03_create_gold_tables.sql
    ├── transformations/
    │   ├── raw_to_silver_usuarios.sql
    │   ├── raw_to_silver_posts.sql
    │   └── silver_to_gold_metricas.sql
    └── data_quality/
        ├── check_usuarios_email.sql
        ├── check_posts_duplicados.sql
        └── check_contagem_registros.sql
```

---

# Configuração do Ambiente

## 1. Criar ambiente e instalar dependências

O Airflow recomenda instalar usando o arquivo de constraints da versão:

```bash
pip install -r requirements.txt --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.7.3/constraints-3.9.txt"
```

---

## 2. Criar banco de dados

*Criar manualmente no PostgreSQL:*

| Parâmetro | Valor |
|---|---|
| Host | `localhost` |
| Porta | `5432` |
| Database | `teste_dados` |
| User | `etl_user` |
| Senha | definida por você |

As credenciais **não ficam no código**. A conexão (`DB_URI`) é montada em `src/config.py` a partir de variáveis de ambiente, carregadas do arquivo `.env` na raiz do projeto (que não é versionado).

Crie o `.env` a partir do modelo e preencha a senha:

```bash
cp .env.example .env
```

```
DB_USER=etl_user
DB_PASSWORD=sua_senha_aqui
DB_HOST=localhost
DB_PORT=5432
DB_NAME=teste_dados
```

---

## 3. Criar tabelas

*Execute os scripts SQL:*

```bash
psql -U etl_user -d teste_dados -f scripts/01_create_raw_tables.sql
psql -U etl_user -d teste_dados -f scripts/02_create_silver_tables.sql
psql -U etl_user -d teste_dados -f scripts/03_create_gold_tables.sql
```

| Camada | Tabela | Chave primária |
|---|---|---|
| RAW | `raw_usuarios`, `raw_posts` | `id` |
| SILVER | `silver_usuarios` | `user_id` |
| SILVER | `silver_posts` | `post_id` |
| GOLD | `gold_metricas_usuario` | `user_id` |

---

## 4. Execução do Pipeline (modo manual)

Como o Airflow não é obrigatório para execução no teste, o pipeline pode ser executado diretamente via Python.
Os comandos devem ser executados **a partir da raiz do projeto**, pois as DAGs leem os SQLs por caminho relativo (`scripts/...`) e importam `src.extract_api`:

```python
from dags.dag_raw_extract import load_usuarios, load_posts
from dags.dag_silver_transform import transform_usuarios, transform_posts
from dags.dag_gold_aggregate import create_metricas_usuario

load_usuarios()
load_posts()

transform_usuarios()
transform_posts()

create_metricas_usuario()
```

---

### Execução via Airflow

*Caso deseje executar via Airflow:*

```bash
airflow db init
airflow webserver --port 8080
airflow scheduler
```

DAGs disponíveis:

| DAG | Agendamento | Tasks |
|---|---|---|
| `etl_raw_extract` | diário às 06:00 | `start >> [extract_usuarios, extract_posts] >> end` |
| `etl_silver_transform` | diário às 06:30 | `start >> [transform_usuarios_task, transform_posts_task] >> end` |
| `etl_gold_aggregate` | diário às 07:00 | `start >> create_metricas_usuario_task >> end` |

Todas usam `catchup=False`, `max_active_runs=1` e `retries=1`.

---

## Funcionamento das Camadas

### RAW (`dags/dag_raw_extract.py` + `src/extract_api.py`)
- Busca os dados na API, achata os campos aninhados do usuário (`address`, `company`) e adiciona a coluna `dl_load_timestamp`.
- Se a API falhar (erro HTTP, resposta inválida ou sem resposta em 30s), a exceção é repassada e a task é marcada como falha, acionando o retry do Airflow.
- Grava com `INSERT ... ON CONFLICT DO NOTHING`: registros cujo `id` já existe na tabela são ignorados. Reexecutar a carga não duplica dados.

### SILVER (`scripts/transformations/raw_to_silver_*.sql`)
- `silver_usuarios`: renomeia colunas e extrai `dominio_email` (texto após o `@`).
- `silver_posts`: remove quebras de linha do conteúdo, trunca em 500 caracteres e calcula `qtd_palavras_titulo`.

### GOLD (`scripts/transformations/silver_to_gold_metricas.sql`)
- Uma linha por usuário com `total_posts`, `media_palavras_titulo` e `primeiro_post_titulo` (post de menor `post_id`).

---

## Data Quality

Foram implementadas validações de qualidade de dados em `scripts/data_quality/`.
Os scripts são executados **manualmente** no banco (não fazem parte das DAGs):

| Script | Validação | Resultado esperado |
|---|---|---|
| `check_contagem_registros.sql` | Contagem entre camadas (RAW -> SILVER -> GOLD) | 10 usuários e 100 posts em cada camada |
| `check_posts_duplicados.sql` | Duplicidade de `post_id` em `silver_posts` | nenhuma linha |
| `check_usuarios_email.sql` | Emails nulos, vazios ou sem `@` em `silver_usuarios` | nenhuma linha |

---

## Observações

- O pipeline pode ser executado manualmente para validação rápida.
- As DAGs são independentes entre si; a ordem RAW -> SILVER -> GOLD é garantida apenas pelos horários de agendamento.
- As três camadas são incrementais: usam `ON CONFLICT DO NOTHING` e apenas inserem registros novos, sem apagar nem atualizar os existentes. O pipeline pode ser reexecutado sem gerar duplicidade.
- Na GOLD, as métricas de um usuário são calculadas na primeira carga e não são recalculadas nas seguintes.
- As DAGs estão estruturadas, mas o ambiente do Airflow (pasta de DAGs, `PYTHONPATH` e usuário do webserver) não está configurado neste repositório. A forma de execução recomendada é o modo manual (seção 4).

## Objetivo do Projeto

Este projeto foi desenvolvido como parte de um teste técnico para avaliação de habilidades em engenharia de dados.
