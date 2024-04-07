import airflow
from airflow import DAG
from airflow.models.variable import Variable
from datetime import datetime
from airflow.providers.apache.hive.hooks.hive import *
from airflow.providers.apache.hive.operators.hive import HiveOperator

init_args = {
    'start_date' : datetime(2024, 4, 4),
}

y_date = Variable.get("y_date")
hive_table = Variable.get("hive_table")


init_dag = DAG(
      dag_id = 'hive_operator', 
      default_args = init_args,  
      schedule_interval = '@daily'
)

hql=(
        f"""
        CREATE EXTERNAL TABLE candle_{y_date} (
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
        LOCATION '/candle/{y_date}';
        """
    )

load_to_hive = HiveOperator(
    task_id="load_to_hive",
    hql=hql,
    dag=init_dag,
    hive_cli_conn_id='hive_cli_default',
)

load_to_hive