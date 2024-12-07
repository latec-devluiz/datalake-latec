from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
import csv
import io
import random
import os
import tempfile  # Para criar um arquivo temporário

# 18:24 - Definição dos argumentos padrão para o DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 11, 29),
}

def gerar_e_enviar_csv():
    # Verificando as variáveis de ambiente
    print("AWS_ACCESS_KEY_ID:", os.getenv("AWS_ACCESS_KEY_ID"))
    print("AWS_SECRET_ACCESS_KEY:", os.getenv("AWS_SECRET_ACCESS_KEY"))
    print("AWS_DEFAULT_REGION:", os.getenv("AWS_DEFAULT_REGION"))
    
    # Gerando dados aleatórios para o CSV
    dados = [
        ['ID', 'Nome', 'Idade', 'Cidade'],
        [1, 'João', random.randint(18, 60), 'São Paulo'],
        [2, 'Maria', random.randint(18, 60), 'Rio de Janeiro'],
        [3, 'Pedro', random.randint(18, 60), 'Belo Horizonte']
    ]

    # Usando io.StringIO para criar o arquivo CSV em memória
    csv_buffer = io.StringIO()
    writer = csv.writer(csv_buffer)
    writer.writerows(dados)

    # Resetando o ponteiro do buffer para o início
    csv_buffer.seek(0)

    # Criando um arquivo temporário para o upload no S3
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(csv_buffer.getvalue().encode())
        temp_filename = temp_file.name

    # Conexão com o S3
    s3_hook = S3Hook(aws_conn_id='aws_default', region_name='us-east-2')

    # Caminho do arquivo no bucket S3
    s3_bucket = 'datalake-latec'
    s3_key = 'raw/teste4.csv'

    # Carregar o arquivo CSV no S3 diretamente do arquivo temporário
    s3_hook.load_file(
        filename=temp_filename,
        key=s3_key,
        bucket_name=s3_bucket,
        replace=True  # Substitui o arquivo no S3 se já existir
    )

    print(f"Arquivo carregado com sucesso em s3://{s3_bucket}/{s3_key}")

# Definindo o DAG
with DAG('gravar_csv', default_args=default_args, schedule_interval=None, catchup=False, ) as dag:
   
   
    # Tarefa que vai gerar o CSV e fazer o upload no S3
    tarefa_gravar_csv = PythonOperator(
        task_id='gerar_e_enviar_csv',
        python_callable=gerar_e_enviar_csv
    )
