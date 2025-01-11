from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

DATABASE_URL = "postgresql+psycopg://andrew:databasepsw@localhost:5432/1amshop" # TODO: delete and place to config

Base = declarative_base()