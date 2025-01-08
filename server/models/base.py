from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

DATABASE_URL = "postgresql+psycopg://andrew:databasepsw@localhost:5432/1amshop"
engine = create_engine(DATABASE_URL, echo=True)

Base = declarative_base()