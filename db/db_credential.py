from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

server = 'L3T2167'
database = 'BoosterPro'
username = 'sa'
password = 'Admin0011##'
driver = 'ODBC+Driver+17+for+SQL+Server'
connection_string = f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver={driver}'

engine = create_engine(connection_string)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine,)
Base = declarative_base()
