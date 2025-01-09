"""
***********************************************
Developer: Tai Sewell

File: database.py

Description: This class is used to create the 
session that the database will be running on.
***********************************************
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = "mysql+pymysql://root:password@db/todo_app"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

"""
***********************************************
Method: User(Base)

Description: This method creates a db session
and then closes the db session when prompted to.
***********************************************
"""
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
