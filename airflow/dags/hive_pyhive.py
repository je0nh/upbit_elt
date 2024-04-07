import airflow
from airflow import DAG
from airflow.models.variable import Variable
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from pyhive import hive

init_args = {
    'start_date' : datetime(2024, 4, 4),
}

y_date = Variable.get("y_date")
hive_table = Variable.get("hive_table")


init_dag = DAG(
      dag_id = 'hive_operator_via_pyhive', 
      default_args = init_args,  
      schedule_interval = '@daily'
)

def load_to_hive(**context):
    host = Variable.get("hdfs_ip_secret")
    port = 10000  # Hive의 기본 포트는 10000입니다.
    username = Variable.get("hive_user_secret")
    database = 'upbit_lake'
    
    conn = hive.Connection(host=host, port=port, username=username, database=database)
    
    hql=(
            f"""
            CREATE EXTERNAL TABLE IF NOT EXISTS candle_{y_date} (
                market STRING,
                candle_date_time_utc STRING,
                candle_date_time_kst STRING,
                opening_price Double,
                high_price Double,
                low_price Double,
                trade_price Double,
                `timestamp` INT,
                candle_acc_trade_price Double,
                candle_acc_trade_volume Double,
                unit INT
            )
            STORED AS PARQUET
            LOCATION '/candle/{y_date}'
            """
        )
    
    # Hive 쿼리 실행
    cursor = conn.cursor()
    cursor.execute(hql)

    # 연결 닫기
    cursor.close()
    conn.close()

load_to_hive = PythonOperator(
    task_id="load_to_hive",
    python_callable=load_to_hive,
    dag=init_dag,
)

load_to_hive
