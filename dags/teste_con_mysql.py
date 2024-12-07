from airflow.hooks.base_hook import BaseHook
from airflow.models import Connection
from airflow.utils.dates import days_ago
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

def test_mysql_connection():
    # Recupera a conexão com o nome 'mysql_libertas'
    connection = BaseHook.get_connection('mysql_libertas')
    
    # Verifique se a conexão foi recuperada corretamente
    if connection:
        print(f"Conexão bem-sucedida: {connection.host}:{connection.port}")
    else:
        print("Falha na conexão.")

# Defina o DAG
dag = DAG(
    'test_mysql_con_dag',
    schedule_interval=None,  # Sem agendamento
    start_date=days_ago(1),
)

# Tarefa de teste da conexão
test_connection_task = PythonOperator(
    task_id='test_connection',
    python_callable=test_mysql_connection,
    dag=dag,
)
