from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
import Database.models
from Database.database import engine, SessionLocal
from sqlalchemy.orm import Session



tdlApp = FastAPI()
Database.models.Base.metadata.create_all(bind=engine)


class ListBase(BaseModel):
    """
    This class serves as the base model of
    what the list's will contain within them.

    @attrib title : Title of list
    @attrib content : Tasks within the list
    @attrib user_id : Used to uniquely identify a list and which user it belongs to
    """
    title: str
    content: str
    user_id: int

class UserBase(BaseModel):
    """
    This class serves as the base model of
    what the user's will contain within them.

    @attrib username : Unique name for each user
    """
    username: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]