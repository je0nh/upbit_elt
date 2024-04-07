# 이어드림 3기 Data Engineering project - develop
- 본 프로젝트 기간: 23.8.29 ~ 23.9.12 (2주)
- 개발 인원: 4명 (박태근, 김민규, 이정훈, 정의찬)
    
  |이름|역할|
  |---|---|
  |박태근|Web socket, Kafka server, Tableau|
  |김민규|Deep learning server, Flask|
  |이정훈|API, Airflow server, MySQL server|
  |정의찬|MySQL server, Hadoop server, Hive|
  
- Develop 기간: 24.3.18 ~ 24.4.7 (3주)

# 프로젝트 목표
- Upbit candle 데이터를 이용한 ELT 파이프라인 구축
- 데이터 수집부터 시각화까지 데이터 파이프라인의 end-to-end 구현
- 자동화 파이프라인 구축

# Architecture
- 본 프로젝트

  <img width="700" alt="Screenshot 2024-04-07 at 10 48 15 PM" src="https://github.com/je0nh/upbit_elt/assets/145730125/d67414d4-1ba8-4773-9934-a3773fc8e7e2">

- Develop

  <img width="600" alt="Screenshot 2024-04-07 at 11 09 55 PM" src="https://github.com/je0nh/upbit_elt/assets/145730125/cbfb9544-e5f6-45a9-902a-db6cb9935ccb">

  - 본 프로젝트와 비교해서 Hadoop을 기준으로 필요없는 DB 제거
  - API 데이터를 HDFS로 전달할때 기존엔 SCP를 사용해서 데이터를 전달 -> 데이터 전송시간이 느림, 데이터 무결성과 보안문제

    <img width="800" alt="Screenshot 2024-04-07 at 11 23 39 PM" src="https://github.com/je0nh/upbit_elt/assets/145730125/c7313ad9-ed44-417b-85c9-05dee1221fa9">
    
  - SCP를 이용한 전달 대신 python 라이브러리인 hdfs를 사용하여 데이터를 전달
    <img width="500" alt="Screenshot 2024-04-07 at 11 24 16 PM" src="https://github.com/je0nh/upbit_elt/assets/145730125/ee46d413-491b-4633-899d-919c20ecf084">
    
  - Airflow의 variable과 Xcom을 사용해 해당하는 날짜의 디렉토리를 만들고 자동으로 해당하는 날짜에 candle 데이터를 저장
  - variable secret를 이용해 보안에 민감할 수 있는 변수 숨김

# 프로젝트 진행과정
1. Upbit에서 데이터를 추출
2. Hadoop을 이용한 Data Lake 구축
3. Hive를 이용한 Data Warehouse 구축
4. Flask를 통해 Hive에서 데이터를 가져와 candle 예측량 계산 -> 예측한 데이터 저장
5. Tableau를 이용한 시각화

## Stack

**Environment** <br>
<img src="https://img.shields.io/badge/jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white">
<img src="https://img.shields.io/badge/git-F05032?style=for-the-badge&logo=git&logoColor=white">
<img src="https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white">

**Language** <br>
<img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white">

**Config** <br>
<img src="https://img.shields.io/badge/amazonec2-FF9900?style=for-the-badge&logo=amazonec2&logoColor=white">
<img src="https://img.shields.io/badge/ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white">
<img src="https://img.shields.io/badge/docker-2496ED?style=for-the-badge&logo=docker&logoColor=white">

**Framework** <br>
<img src="https://img.shields.io/badge/apacheairflow-017CEE?style=for-the-badge&logo=apacheairflow&logoColor=white">
<img src="https://img.shields.io/badge/apachehadoop-66CCFF?style=for-the-badge&logo=apachehadoop&logoColor=white">
<img src="https://img.shields.io/badge/flask-000000?style=for-the-badge&logo=flask&logoColor=white">
<img src="https://img.shields.io/badge/tableau-E97627?style=for-the-badge&logo=tableau&logoColor=white">
