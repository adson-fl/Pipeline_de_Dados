from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from sqlalchemy import create_engine, text

from src.config import DB_URI

default_args = {
    "owner": "etl_user",
    "retries": 1
}

def run_sql_file(file_path):
    engine = create_engine(DB_URI)

    with open(file_path, "r") as file:
        sql = file.read()
    
    with engine.begin() as conn:
        conn.execute(text(sql))

def create_metricas_usuario():
    run_sql_file("scripts/transformations/silver_to_gold_metricas.sql")

with DAG(
    dag_id="etl_gold_aggregate",
    default_args=default_args,
    schedule_interval="0 7 * * *", #Diario as 7h 
    start_date=datetime(2024, 1, 1), 
    catchup=False,
    max_active_runs=1,
    tags=["gold", "aggregate", "analytics"]
) as dag:
    start = PythonOperator(
        task_id="start",
        python_callable=lambda: print("Iniciando camada GOLD")
    )

    create_metricas_usuario_task = PythonOperator(
        task_id="create_metricas_usuario_task",
        python_callable=create_metricas_usuario
    )

    end = PythonOperator(
        task_id="end",
        python_callable=lambda: print("Finalizando camada GOLD")
    )
    start >> [create_metricas_usuario_task] >> end