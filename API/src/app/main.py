"""
***********************************************
Developer: Tai Sewell

File: main.py

Description: File that contains the main API.
***********************************************
"""
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from Database.src import models, database
from .routes import users, tasks
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager


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
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    models.Base.metadata.create_all(bind=database.engine)
    yield

tdlapp = FastAPI(lifespan=lifespan)

# Add CORS middleware
tdlapp.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Include routers from separate files
tdlapp.include_router(users.router)
tdlapp.include_router(tasks.router)


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
    return "Welcome to my To-Do List API!"