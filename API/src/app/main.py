from fastapi import FastAPI, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session
from Database.src import models, database

tdlapp = FastAPI()

# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@tdlapp.on_event("startup")
def startup():
    models.Base.metadata.create_all(bind=database.engine)

@tdlapp.get("/tables")
def list_tables(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SHOW TABLES"))
        tables = [row[0] for row in result]
        return {"tables": tables}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@tdlapp.get("/test-db-connection")
def test_db_connection(db: Session = Depends(get_db)):
    try:
        # Execute a simple query to test the connection
        db.execute(text("SELECT 1"))
        return {"status": "Connection successful"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@tdlapp.get("/")
def read_root():
    return {"Hello": "World"}

@tdlapp.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@tdlapp.post("/users/")
async def create_user(request: Request, db: Session = Depends(get_db)):
    user_data = await request.json()
    username = user_data.get("username")
    hashed_password = user_data.get("hashed_password")

    if not username or not hashed_password:
        raise HTTPException(status_code=400, detail="Username and hashed_password are required")

    db_user = models.User(username=username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

