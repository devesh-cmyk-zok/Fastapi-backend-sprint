from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address>/<database_name>'

# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Devpsql321%23@localhost:5432/postgres'

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

base = declarative_base()


def get_db():
    db = SessionLocal()  # create a new session
    try:
        yield db  # yield the session to the caller
    finally:
        db.close()  # close the session after the request is done