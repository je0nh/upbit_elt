from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Double, BigInteger
from sqlalchemy.exc import OperationalError, IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from upbit_api import upbit
import time

class UpbitDb:
    def __init__(self, id, pw, ip, port, db):
        self.id = id
        self.pw = pw
        self.ip = ip
        self.port = port
        self.db = db

    def conn(self):
        db_path = f'mysql://{self.id}:{self.pw}@{self.ip}:{self.port}/{self.db}'

        self.engine = create_engine(db_path, pool_pre_ping=True)

        try:
            # 연결 시도
            with self.engine.connect():
                print("Database connection successful.")
        except OperationalError as e:
            print(f"Database connection failed. Error: {e}")

        return self.engine.connect()
    
    def market_meta(self, table):
        Base = declarative_base()

        # 모델 클래스 정의
        class MarketMetadata(Base):
            __tablename__ = table

            market_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
            market = Column(String, nullable=False)
            korean_name = Column(String, nullable=False)
            english_name = Column(String, nullable=False)

        # 테이블 생성
        Base.metadata.create_all(self.engine)

        # 세션 생성
        Session = sessionmaker(bind=self.engine)
        session = Session()
        
        coin = upbit.Api()
        market_code = coin.market_code()
        
        # 딕셔너리를 모델 객체로 변환하여 데이터베이스에 추가
        for data in market_code:
            new_entry = MarketMetadata(**data)
            try:
                session.add(new_entry)
                session.commit()
            except IntegrityError:
                pass
        return print('Update Market code matadata upload!')
    
    def candle(self, table, fk_table, type, data):
        Base = declarative_base()
        
        if type == 'minutes':
            class Candle(Base):
                __tablename__ = table
                
                candle_id = Column(Integer, primary_key=True, nullable=False)
                market = Column(Integer, nullable=False)
                candle_date_time_utc = Column(String, nullable=False)
                candle_date_time_kst = Column(String, nullable=False)
                opening_price = Column(Double, nullable=False)
                high_price = Column(Double, nullable=False)
                low_price = Column(Double, nullable=False)
                trade_price = Column(Double, nullable=False)
                timestamp = Column(BigInteger, nullable=False)
                candle_acc_trade_price = Column(Double, nullable=False)
                candle_acc_trade_volume = Column(Double, nullable=False)
                unit = Column(Integer, nullable=False)
        
        elif type == 'days':
            class Candle(Base):
                __tablename__ = table
                
                candle_id = Column(Integer, primary_key=True,  nullable=False)
                market = Column(Integer, ForeignKey(fk_table), nullable=False)
                candle_date_time_utc = Column(String, nullable=False)
                candle_date_time_kst = Column(String, nullable=False)
                opening_price = Column(Double, nullable=False)
                high_price = Column(Double, nullable=False)
                low_price = Column(Double, nullable=False)
                trade_price = Column(Double, nullable=False)
                timestamp = Column(BigInteger, nullable=False)
                candle_acc_trade_price = Column(Double, nullable=False)
                candle_acc_trade_volume = Column(Double, nullable=False)
                prev_closing_price = Column(Double, nullable=False)
                change_price = Column(Double, nullable=False)
                change_rate = Column(Double, nullable=False)
                converted_trade_price = Column(Double, nullable=False)
        
        else:
            class Candle(Base):
                __tablename__ = table
                
                candle_id = Column(Integer, primary_key=True,  nullable=False)
                market = Column(Integer, ForeignKey(fk_table), nullable=False)
                candle_date_time_utc = Column(String, nullable=False)
                candle_date_time_kst = Column(String, nullable=False)
                opening_price = Column(Double, nullable=False)
                high_price = Column(Double, nullable=False)
                low_price = Column(Double, nullable=False)
                trade_price = Column(Double, nullable=False)
                timestamp = Column(BigInteger, nullable=False)
                candle_acc_trade_price = Column(Double, nullable=False)
                candle_acc_trade_volume = Column(Double, nullable=False)
                first_day_of_period = Column(String, nullable=False)
        
        # 테이블 생성
        Base.metadata.create_all(self.engine)

        # 세션 생성
        Session = sessionmaker(bind=self.engine)
        session = Session()

        # 딕셔너리를 모델 객체로 변환하여 데이터베이스에 추가
        new_entry = Candle(**data)
        session.add(new_entry)
        session.commit()