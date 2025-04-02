"""
***********************************************
Developer: Tai Sewell

File: database.py

Description: This file contains the DB connection.
***********************************************
"""

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
