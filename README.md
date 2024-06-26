# Data Engineering project - develop
- 프로젝트 기간: 24.3.18 ~ 24.4.7 (3주)

# 프로젝트 목표
- Upbit candle 데이터를 이용한 ELT 파이프라인 구축
- 데이터 수집부터 시각화까지 데이터 파이프라인의 end-to-end 구현
- 자동화 파이프라인 구축

# Architecture

<img width="600" alt="Screenshot 2024-04-08 at 2 50 24 AM" src="https://github.com/je0nh/upbit_elt/assets/145730125/0b07056f-42df-42d7-b8a3-916a6970a426">

    
  - python 라이브러리인 hdfs를 사용하여 데이터를 전달
    ```python
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
    ```

  - HDFS에 데이터 저장시 parquet 포멧 사용
  - Airflow의 variable과 XComs을 사용해 해당하는 날짜의 디렉토리를 만들고 자동으로 해당하는 날짜에 candle 데이터를 저장
      - variable
 
       	<img width="700" alt="Screenshot 2024-04-08 at 1 05 43 AM" src="https://github.com/je0nh/upbit_elt/assets/145730125/02401fea-699c-41a6-bfb1-f3feb893e110">

        
      - XComs

		<img width="700" alt="Screenshot 2024-04-08 at 1 06 23 AM" src="https://github.com/je0nh/upbit_elt/assets/145730125/05f7ce62-c785-4340-b543-067f8477c969">


  - variable secret를 이용해 보안에 민감할 수 있는 변수 숨김
    <img width="700" alt="Screenshot 2024-04-08 at 1 04 46 AM" src="https://github.com/je0nh/upbit_elt/assets/145730125/3866a57a-cdf4-4c8d-9037-36aa7b34dc90">


# 프로젝트 진행과정
1. Upbit에서 데이터를 추출
    - Code spinet (upbit.py)
        ```python
        ...
        def candles(self, type: str, market: str, unit=1, to='', count=1, convertingPriceUnit='KRW') -> list:
            if type == 'minutes':
                quotation = f'candles/{type}/1?market={market}&unit={unit}&to={to}&count={count}&convertingPriceUnit={convertingPriceUnit}'
            elif type == 'days':
                quotation = f'candles/{type}/1?market={market}&to={to}&count={count}&convertingPriceUnit={convertingPriceUnit}'
            else:
                quotation = f'candles/{type}/1?market={market}&to={to}&count={count}'
            response = self.call(quotation)
            return response.json()
        ...
        ```
3. Airflow를 활용해 설정한 시간마다 배치 단위로 데이터 처리, Xcom을 이용한 파일 이름 변수 전달
   - Code spinet (min_dag.py)
        ```python
        ...
        init_dag = DAG(
          dag_id = 'min_candle', 
          default_args = init_args,  
          schedule_interval = '*/2 * * * * '
        )
        ...
        ```
    - Code spinet (min_dag.py)
      ```python
      ...
      # def min_candle
      context['task_instance'].xcom_push(key='file_name', value=file_name)
      context['task_instance'].xcom_push(key='local_file_path', value=local_file_path)
      ...
      # def to_hdfs
      file_name = context['task_instance'].xcom_pull(key='file_name')
      local_file_path = context['task_instance'].xcom_pull(key='local_file_path')
      ...
4. Hadoop을 이용한 Data Lake 구축
   - Docker image build
     
       <img width="500" alt="Screenshot 2024-04-08 at 1 13 48 AM" src="https://github.com/je0nh/upbit_elt/assets/145730125/fbe98078-6fdc-4a8a-9e76-b42b0e4a1801">


    - yarn-site.xml
        ```xml
        <property>
            <name>yarn.nodemanager.resource.cpu-vcores</name>
            <value>2</value>
        </property>
        <property>
            <name>yarn.nodemanager.resource.memory-mb</name>
            <value>3072</value>
        </property>
        ```

        <img width="700" alt="Screenshot 2024-04-08 at 12 34 33 AM" src="https://github.com/je0nh/upbit_elt/assets/145730125/252ce7e0-18a3-457d-80ee-05cc7c5b7620">


    - hdfs-site.xml (datanode)
        ```xml
        <property>
            <name>dfs.datanode.du.reserved</name>
            <value>319856951951</value>
        </property>
        ```

        <img width="700" alt="Screenshot 2024-04-08 at 12 32 12 AM" src="https://github.com/je0nh/upbit_elt/assets/145730125/3eb60e0c-2d78-48ab-b1ae-0c9d57d5b8f6">

    
6. 날짜가 바뀌면 variable에 해당 날짜와 전날의 날짜 저장
    - Code spinet (min_dag.py)
        ```python
        ...
        if sys_date == var_date:
            hdfs_file_path = f'{hdfs_path_secret}/{var_date}/{file_name}'
        else:
            Variable.set("y_date", var_date)
            Variable.set("to_date", sys_date)
            client.makedirs(f'{hdfs_path_secret}/{sys_date}')
            hdfs_file_path = f'{hdfs_path_secret}/{sys_date}/{file_name}'
        ...
        ```
    - Airflow variable
      
      <img width="700" alt="Screenshot 2024-04-08 at 12 35 40 AM" src="https://github.com/je0nh/upbit_elt/assets/145730125/0159d23c-36e6-465e-9d09-fa005ed329a0">

    - HDFS
      
      <img width="700" alt="Screenshot 2024-04-08 at 12 36 59 AM" src="https://github.com/je0nh/upbit_elt/assets/145730125/100b4c98-2885-44d2-9569-44f018872346">
      
      <img width="700" alt="Screenshot 2024-04-08 at 12 42 39 AM" src="https://github.com/je0nh/upbit_elt/assets/145730125/d5f98098-bd09-45bc-98a7-824ad3f92e64">


7. Hive를 이용한 Data Warehouse 구축
8. Hive로 데이터 자동 업로드
   - Code spinet (hive_pyhive.py)
       ```python
       ...
       def load_to_hive(**context):
            host = Variable.get("hdfs_ip_secret")
            port = 10000
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
       
            cursor = conn.cursor()
            cursor.execute(hql)
       
            cursor.close()
            conn.close()
       ...
       ```

    - Hive SQL
        ```SQL
        SELECT market , candle_date_time_utc , candle_date_time_kst , opening_price
        FROM candle_240407
        WHERE market = 'KRW-BTC';
        ```

        <img width="700" alt="Screenshot 2024-04-08 at 12 41 14 AM" src="https://github.com/je0nh/upbit_elt/assets/145730125/f2e4d1aa-f565-45cb-a971-b5873ce0a424">

        
10. Tableau를 이용한 시각화
    
    <img width="651" alt="Screenshot 2024-04-07 at 11 53 14 PM" src="https://github.com/je0nh/upbit_elt/assets/145730125/424ff29d-d4b4-4e86-8ba7-dac5f2ffe27c">
    <img width="646" alt="Screenshot 2024-04-07 at 11 53 23 PM" src="https://github.com/je0nh/upbit_elt/assets/145730125/0fc7eb0e-2a8c-47f0-b131-e3198d23c864">



# Stack

**Environment** <br>
<img src="https://img.shields.io/badge/jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white">
<img src="https://img.shields.io/badge/git-F05032?style=for-the-badge&logo=git&logoColor=white">
<img src="https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white">

**Language** <br>
<img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white">

**Config** <br>
<img src="https://img.shields.io/badge/ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white">
<img src="https://img.shields.io/badge/docker-2496ED?style=for-the-badge&logo=docker&logoColor=white">

**Framework** <br>
<img src="https://img.shields.io/badge/apacheairflow-017CEE?style=for-the-badge&logo=apacheairflow&logoColor=white">
<img src="https://img.shields.io/badge/apachehadoop-66CCFF?style=for-the-badge&logo=apachehadoop&logoColor=white">
<img src="https://img.shields.io/badge/tableau-E97627?style=for-the-badge&logo=tableau&logoColor=white">

# 프로젝트 한계
1. Hadoop(jdk-11)과 Hive(jdk-8) jdk version 차이로 인해 Hive에서 MR을 할수 없음 -> Hive 4.0.0 버전이 새로 출시 됨에 따라, Hadoop 3.3.6에서 사용가능할 것으로 생각함

    ```bash
	org.jkiss.dbeaver.model.sql.DBSQLException: SQL Error [2] [08S01]: Error while processing statement: FAILED: Execution Error, return code 2 from org.apache.hadoop.hive.ql.exec.mr.MapRedTask
	...
	Caused by: java.sql.SQLException: Error while processing statement: FAILED: Execution Error, return code 2 from org.apache.hadoop.hive.ql.exec.mr.MapRedTask
	...
    ```

    <img width="593" alt="Screenshot 2024-04-08 at 12 51 15 AM" src="https://github.com/je0nh/upbit_elt/assets/145730125/bb69f647-c8cf-43a7-9562-4368e442b066">

2. Airflow에서 Hiveconnector 사용할수 없었음 -> pyhive를 사용해 대체
   ```bash
   Traceback (most recent call last):
	  File "/home/airflow/.local/lib/python3.8/site-packages/airflow/models/taskinstance.py", line 444, in _execute_task
	    result = _execute_callable(context=context, **execute_callable_kwargs)
	  File "/home/airflow/.local/lib/python3.8/site-packages/airflow/models/taskinstance.py", line 414, in _execute_callable
	    return execute_callable(context=context, **execute_callable_kwargs)
	  File "/home/airflow/.local/lib/python3.8/site-packages/airflow/providers/apache/hive/operators/hive.py", line 166, in execute
	    self.hook.run_cli(hql=self.hql, schema=self.schema, hive_conf=self.hiveconfs)
	  File "/home/airflow/.local/lib/python3.8/site-packages/airflow/providers/apache/hive/hooks/hive.py", line 292, in run_cli
	    sub_process: Any = subprocess.Popen(
	  File "/usr/local/lib/python3.8/subprocess.py", line 858, in __init__
	    self._execute_child(args, executable, preexec_fn, close_fds,
	  File "/usr/local/lib/python3.8/subprocess.py", line 1720, in _execute_child
	    raise child_exception_type(errno_num, err_msg, err_filename)
   PermissionError: [Errno 13] Permission denied: 'beeline'
   ```

