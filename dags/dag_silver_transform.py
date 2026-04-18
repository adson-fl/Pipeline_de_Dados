from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from sqlalchemy import create_engine, text

DB_URI = "postgresql://etl_user:SENHA_REMOVIDA@localhost:5432/teste_dados"

# Função generica
def run_sql_file(file_path):
    engine = create_engine(DB_URI) # conexão com o banco

    with open(file_path, "r") as file:
        sql = file.read() # ler

    with engine.connect() as conn: # abrir conexão com o banco
        conn.execute(text(sql)) # insert do excript sql 
    

# tasks
def transform_usuarios():
    run_sql_file("scripts/transformations/raw_to_silver_usuarios.sql")

def transform_posts():
    run_sql_file("scripts/transformations/raw_to_silver_posts.sql")

# DAG
with DAG (
    dag_id= "etl_silver_transform",
    schedule_interval="30 6 * * *",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    max_active_runs=1,
    tags=["silver", "transfor"]
) as dag:
    
    start = PythonOperator(
        task_id ="start",
        python_callable=lambda: print("Iniciando camada SILVER")
    )

    transform_usuarios_task = PythonOperator(
        task_id="transform_usuarios_task",
        python_callable= transform_usuarios
    )

    transform_posts_task = PythonOperator(
        task_id="transform_posts_task",
        python_callable=transform_posts
    )

    end = PythonOperator(
        task_id="end",
        python_callable=lambda: print("Finalizando camada SILVER")
    )

    start >> [transform_usuarios_task, transform_posts_task] >> end
    