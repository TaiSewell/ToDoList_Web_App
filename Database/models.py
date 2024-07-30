from sqlalchemy import Boolean, Column, Integer, String
from database import Base

class User(Base):
    """
    This class is used to store the users
    in a table name users.

    @attrib __tablename__ : Names the Table
    @attrib username : This will be used to store the usernames uniquely
    """
    __tablename__ = 'users'
    username = Column(String(50), unique=True)

class List(Base):
    """
    This class is used to store the lists
    in a table name lists.

    @attrib __tablename__ : Names the Table
    @attrib id : Used to store lists at uniquely index locations
    @attrib title : This will be the name of the list that is stored
    @attrib content : This will be the tasks stored within the list
    """
    __tablename__= 'lists'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50))
    content = Column(String(100))
    user_id = Column(Integer)

