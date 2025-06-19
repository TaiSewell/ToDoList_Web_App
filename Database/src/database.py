"""
***********************************************
Developer: Tai Sewell

File: database.py

Description: This class is used to create the 
session that the database will be running on.
***********************************************
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../../.env'))

# Access database connection variables from environment
DATABASE_URL = os.getenv("DATABASE_URL")

# Ensure DATABASE_URL is set
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in environment variables")

print(f"Connecting to MySQL database with URL: {DATABASE_URL}")

# SQLAlchemy engine for connecting to the database
engine = create_engine(DATABASE_URL)

# Declarative Base for defining models
Base = declarative_base()

# Create a session factory for making database connections
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()