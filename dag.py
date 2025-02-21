from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import subprocess

# Define default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 2, 17),
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'run_python_script',
    default_args=default_args,
    description='A DAG to run a python ETL job',
    schedule_interval=timedelta(days=1)
)

# Define the task to run the Python script
def run_script():
    subprocess.run(["python3", "/home/brian.canyon/Documents/rpi4/ETL_script.py"], check=True)

run_script_task = PythonOperator(
    task_id='run_script',
    python_callable=run_script,
    dag=dag,
)

# Set the task dependencies (single, as example)
run_script_task