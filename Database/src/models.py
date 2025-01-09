"""
***********************************************
Developer: Tai Sewell

File: models.py

Description: This class is used to create tables
for the database.
***********************************************
"""
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .database import Base


"""
***********************************************
Class: User(Base)

Description: This class is used to create a
table for users.
***********************************************
"""
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    tasks = relationship("Task", back_populates="owner")

"""
***********************************************
Class: User(Base)

Description: This class is used to create a
table for users.
***********************************************
"""
class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="tasks")