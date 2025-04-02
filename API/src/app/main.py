"""
***********************************************
Developer: Tai Sewell

File: main.py

Description: File that contains the main API.
***********************************************
"""


from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy import text
from sqlalchemy.orm import Session
from Database.src import models, database
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
import secrets
from routes import users, auth


tdlapp = FastAPI()

# Include Routes from auth
tdlapp.include_router(users.router, prefix="/users", tags=["users"])
tdlapp.include_router(auth.router, prefix="/auth", tags=["auth"])

"""
***********************************************
Method: list_tables()


Description: This method is used to show all the 
tables that are within the database.

returns: A welcome message.
***********************************************
"""
@tdlapp.get("/tables")
def list_tables(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SHOW TABLES"))
        tables = [row[0] for row in result]
        return {"tables": tables}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



"""
***********************************************
Method: read_root()


Description: This method is used to test the 
root(/) endpoint.

returns: A welcome message.
***********************************************
"""
@tdlapp.get("/")
def read_root():
    return "Welcome to my To-Do List API!"

