import os

from sqlalchemy import create_engine, URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

if not os.getenv('DRIVER') or os.getenv('DRIVER') == 'sqlite':
    SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db?check_same_thread=False"
    # SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
elif not (os.getenv('DB_USER_NAME') and os.getenv('DB_PASSWORD')):
    SQLALCHEMY_DATABASE_URL = URL.create(drivername=os.getenv('DRIVER'),
                                         username=os.getenv('DB_USER_NAME'),
                                         password=os.getenv('DB_PASSWORD'),
                                         host=os.getenv('DB_HOST', '0.0.0.0'),
                                         database=os.getenv('DB_NAME', 'chat')
                                         )
else:
    SQLALCHEMY_DATABASE_URL = URL.create(drivername=os.getenv('DRIVER'),
                                         username=os.getenv('DB_USER_NAME'),
                                         password=os.getenv('DB_PASSWORD'),
                                         host=os.getenv('DB_HOST', '0.0.0.0'),
                                         database=os.getenv('DB_NAME', 'chat')
                                         )
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
