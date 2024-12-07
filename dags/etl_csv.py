from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
import mysql.connector
import csv
import io  # Para trabalhar com arquivos em memória

# 16:25 Definição dos argumentos padrão para o DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 11, 29),  # Data de início
}

def test_mysql_connection_and_upload_to_s3():
    connection = None  # Inicializa a conexão como None
    try:
        # Estabelecendo a conexão com o banco MySQL
        connection = mysql.connector.connect(
            host='77.37.68.185',  # Endereço do servidor
            database='libertas',  # Nome do banco de dados
            user='myluiz',  # Usuário
            password='785612'  # Senha
        )

        if connection.is_connected():
            print("Conexão bem-sucedida com o MySQL")
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM teste;')  # Selecionando todos os registros da tabela 'teste'
            result = cursor.fetchall()  # Obtendo todos os resultados

            # Usando io.StringIO para escrever em memória (sem salvar localmente)
            csv_buffer = io.StringIO()
            writer = csv.writer(csv_buffer)
            # Escreve o cabeçalho com os nomes das colunas
            writer.writerow([desc[0] for desc in cursor.description])
            # Escreve os dados retornados pela consulta
            writer.writerows(result)

            # Retorna o ponteiro para o início do buffer
            csv_buffer.seek(0)

            # Agora, faz o upload para o S3
            s3_hook = S3Hook(aws_conn_id='aws_default')  # 'aws_default' é o nome da conexão configurada no Airflow

            # Caminho do arquivo no bucket S3
            s3_bucket = 'datalake-latec'
            s3_key = 'raw/teste_mysql.csv'

            # Carregar o arquivo no S3 diretamente do buffer em memória
            s3_hook.load_file(
                file_obj=csv_buffer,
                key=s3_key,
                bucket_name=s3_bucket,
                replace=True  # Substitui o arquivo no S3 se já existir
            )
            print(f"Arquivo carregado para o S3 em s3://{s3_bucket}/{s3_key}")

            cursor.close()

    except mysql.connector.Error as e:
        print("Erro ao conectar ao MySQL", e)
    except Exception as e:
        print("Erro inesperado", e)
    finally:
        # Verifique se a conexão foi criada antes de tentar fechá-la
        if connection and connection.is_connected():
            connection.close()

# Definição do DAG
with DAG(
    'etl_mysql_to_s3',
    default_args=default_args,
    schedule_interval=None,  # Define como None, ou seja, não será executado automaticamente
    catchup=False,  # Não irá executar as execuções passadas
) as dag:

    # Tarefa que irá executar a função de teste de conexão, gravar o CSV e enviar para o S3
    test_connection_and_upload = PythonOperator(
        task_id='test_mysql_connection_and_upload_to_s3',
        python_callable=test_mysql_connection_and_upload_to_s3  # Função que fará a consulta, gravação e upload
    )
