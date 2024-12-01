from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())
connection = os.getenv("CONNECTION")

engine = create_engine(connection, echo=True, pool_pre_ping=True)


def get_db_session():
    with Session(bind=engine) as session:
        yield session
