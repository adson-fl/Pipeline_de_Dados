from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from sqlalchemy import create_engine

from src.extract_api import extract_usuarios, extract_posts

default_args = {
    "owner": "etl_user",
    "retries": 1
}
DB_URI = "postgresql://etl_user:SENHA_REMOVIDA@localhost:5432/teste_dados"

def load_usuarios():
    df = extract_usuarios()
    engine = create_engine(DB_URI) # conexão com o banco
    df.to_sql("raw_usuarios", engine, if_exists="append", index=False) # nserção dos usuarios com o banco

def load_posts():
    df = extract_posts()
    engine = create_engine(DB_URI)
    df.to_sql("raw_posts", engine, if_exists="append", index=False) # inserção dos posts com o banco


with DAG(
    dag_id="etl_raw_extract",
    schedule_interval="0 6 * * *", # horario de atualização
    start_date=datetime(2024, 1, 1), # data inicial 
    catchup=False,
    max_active_runs=1,
    tags=["raw", "extract", "api"]
) as dag:
    
    start = PythonOperator(
        task_id ="start",
        python_callable=lambda: print("Iniciando pipeline RAW")
    )
    extract_usuarios_task = PythonOperator(
        task_id ="extract_usuarios",
        python_callable=load_usuarios
    )
    extract_posts_task = PythonOperator(
        task_id="extract_posts",
        python_callable=load_posts
    )
    end = PythonOperator(
        task_id="end",
        python_callable=lambda: print("Finalizando pipeline RAW")
    )
    start >> [extract_usuarios_task, extract_posts_task] >> end # dependencia do grafo