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
    username = Column(String(50), unique=True, index=True, nullable=False)  # Specify length for VARCHAR
    hashed_password = Column(String(100), nullable=False)                   # Specify length for VARCHAR

    tasks = relationship("Task", back_populates="owner")

"""
***********************************************
Class: Task(Base)

Description: This class is used to create a
table for tasks.
***********************************************
"""
class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)                             # Specify length for VARCHAR
    description = Column(String(255))                                       # Specify length for VARCHAR
    owner_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship("User", back_populates="tasks")