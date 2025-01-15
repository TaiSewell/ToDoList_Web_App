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

tdlapp = FastAPI()

"""
***********************************************
Method: get_db()

Description: This method is used to fetch the 
database session and close it when it is done.

returns: N/A
***********************************************
"""
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

"""
***********************************************
Method: startup()


Description: This method is used to populate 
the database with the tables that are defined 
in Database/src/models.py. from the start.

returns: N/A
***********************************************
"""
@tdlapp.on_event("startup")
def startup():
    models.Base.metadata.create_all(bind=database.engine)


"""
***********************************************
Method: list_tables()


Description: This method is used to display the 
tables that are currently within the database.

returns: The table models that are in the
database.
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
Method: test_db_connection()


Description: This method is used to send a get
request to the database to test the connection.

returns: A message indicating the status of the
connection.
***********************************************
"""
@tdlapp.get("/test-db-connection")
def test_db_connection(db: Session = Depends(get_db)):
    try:
        # Execute a simple query to test the connection
        db.execute(text("SELECT 1"))
        return {"status": "Connection successful"}
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
    return "Welcome to the To-Do List API!"


"""
***********************************************
Method: read_user()


Description: This method is used to retrieve a user
based on the user_id from the database.

returns: A user object.
***********************************************
"""
@tdlapp.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

"""
***********************************************
Method: create_user()


Description: This method is used to create a user
in the database.

returns: The created user object.
***********************************************
"""
@tdlapp.post("/users/")
async def create_user(request: Request, db: Session = Depends(get_db)):
    user_data = await request.json()
    username = user_data.get("username")
    hashed_password = user_data.get("hashed_password")

    if not username or not hashed_password:
        raise HTTPException(status_code=400, detail="Username and hashed_password are required")

    existing_user = db.query(models.User).filter(models.User.username == username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    db_user = models.User(username=username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

