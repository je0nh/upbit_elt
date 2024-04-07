import airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.models.variable import Variable
from upbit_api import upbit
from datetime import datetime, timezone, timedelta
import pendulum
import pandas as pd
from hdfs import InsecureClient
import os

hdfs_ip_secret = Variable.get("hdfs_ip_secret")
hdfs_port_secret = Variable.get("hdfs_port_secret")
hdfs_id_secret = Variable.get("hdfs_id_secret")
hdfs_path_secret = Variable.get("hdfs_path_secret")

upbit = upbit.Api()
KST = timezone(timedelta(hours=9))
now = datetime.now(KST)

local_tz = pendulum.timezone("Asia/Seoul")

init_args = {
    'start_date' : datetime(2024, 4, 4, tzinfo=local_tz),
    "provide_context":True
}

init_dag = DAG(
      dag_id = 'min_candle', 
      default_args = init_args,  
      schedule_interval = '*/2 * * * * '
)

def min_candle(**context):
    sys_date = now.strftime('%y%m%d%H%M%S')

    n = len(upbit.market_code())
    candle_data = []

    for i in range(n):
        market_code = upbit.market_code()[i].get('market')
        candle = upbit.candles(type='minutes', market=market_code)
        candle_data += candle
        
    df = pd.DataFrame(candle_data)

    file_name = f'{sys_date}_candel_data.parquet'
    local_file_path = '/opt/airflow/dags/data/' + file_name
    df.to_parquet(path=local_file_path, index=False)
    
    context['task_instance'].xcom_push(key='file_name', value=file_name)
    context['task_instance'].xcom_push(key='local_file_path', value=local_file_path)

    return print("데이터 크롤링 완료")

def to_hdfs(**context):
    client = InsecureClient(f'http://{hdfs_ip_secret}:{hdfs_port_secret}', user=hdfs_id_secret)

    file_name = context['task_instance'].xcom_pull(key='file_name')
    local_file_path = context['task_instance'].xcom_pull(key='local_file_path')
    
    sys_date = now.strftime('%y%m%d')
    var_date = Variable.get("to_date")
    
    if sys_date == var_date:
        hdfs_file_path = f'{hdfs_path_secret}/{var_date}/{file_name}'
    else:
        Variable.set("y_date", var_date)
        Variable.set("to_date", sys_date)
        client.makedirs(f'{hdfs_path_secret}/{sys_date}')
        hdfs_file_path = f'{hdfs_path_secret}/{sys_date}/{file_name}'

    with open(local_file_path, 'rb') as local_file:
        with client.write(hdfs_file_path) as hdfs_file:
            hdfs_file.write(local_file.read())
        
    os.remove(local_file_path)
    return print("데이터 적재 완료")

task1 = PythonOperator(
    task_id = 'get_min_candle',
    python_callable=min_candle,
    dag = init_dag
)

task2 = PythonOperator(
    task_id = 'to_hdfs',
    python_callable=to_hdfs,
    dag = init_dag
)

task1 >> task2