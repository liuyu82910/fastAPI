from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time
import psycopg2
from psycopg2.extras import RealDictCursor
from .config import settings


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Using psycopg2 to connect to db
def get_psycopg2():
    ct = 0
    while ct < 3:
        try:
            conn = psycopg2.connect(host=f'{settings.database_hostname}', database=f'{settings.database_name}', user=f'{settings.database_username}', password=f'{settings.database_password}', cursor_factory=RealDictCursor)
            print('Database connection established')
            return conn
        except Exception as error:
            print('Connection failed:', error)
            time.sleep(3)
            ct += 1