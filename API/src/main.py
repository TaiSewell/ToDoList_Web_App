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
    return "Welcome to my To-Do List API!"


"""
***********************************************
           All User Endpoints/Methods
***********************************************

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

"""
***********************************************
Method: read_users()

Description: This method is used to fetch all 
users.

returns: A list of users.
***********************************************
"""
@tdlapp.get("/users/")
def read_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

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
Method: delete_user()

Description: This method is used to delete a 
user from the database by their ID.

returns: A message indicating the result.
***********************************************
"""
@tdlapp.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    user_count = db.query(models.User).count()
    if user_count == 0:
        db.execute(text("ALTER TABLE users AUTO_INCREMENT = 1"))
        db.commit()
    
    return {"detail": "User deleted"}


"""
***********************************************
Method: update_user()

Description: This method is used to update a 
user's information.

returns: The updated user details.
***********************************************
"""
@tdlapp.put("/users/{user_id}")
async def update_user(user_id: int, request: Request, db: Session = Depends(get_db)):
    user_data = await request.json()
    username = user_data.get("username")
    hashed_password = user_data.get("hashed_password")

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if username:
        user.username = username
    if hashed_password:
        user.hashed_password = hashed_password

    db.commit()
    db.refresh(user)
    return user

"""
***********************************************
           All Task Endpoints/Methods
***********************************************

***********************************************
Method: create_task()


Description: This method is used to create a task
in the database.

returns: The created task object.
***********************************************
"""
@tdlapp.post("/tasks/")
async def create_task(request: Request, db: Session = Depends(get_db)):
    task_data = await request.json()
    title = task_data.get("title")
    description = task_data.get("description")
    owner_id = task_data.get("owner_id")
    
    users = db.query(models.User).all()
    if not users:
        raise HTTPException(status_code=404, detail="No users found")

    if not title or not owner_id:
        raise HTTPException(status_code=400, detail="Title and owner_id are required")

    db_task = models.Task(title=title, description=description, owner_id=owner_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

"""
***********************************************
Method: read_task()

Description: This method is used to retrieve a task
based on the task_id from the database.

returns: A task object.
***********************************************
"""
@tdlapp.get("/tasks/{task_id}")
def read_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

"""
***********************************************
Method: read_tasks()

Description: This method is used to fetch all 
tasks.

returns: A list of tasks.
***********************************************
"""
@tdlapp.get("/tasks/")
def read_tasks(db: Session = Depends(get_db)):
    tasks = db.query(models.Task).all()
    return tasks

"""
***********************************************
Method: read_tasks_by_user()

Description: This method is used to fetch all 
tasks for a specific user.

returns: A list of tasks.
***********************************************
"""
@tdlapp.get("/users/{user_id}/tasks/")
def read_tasks_by_user(user_id: int, db: Session = Depends(get_db)):
    tasks = db.query(models.Task).filter(models.Task.owner_id == user_id).all()
    return tasks

"""
***********************************************
Method: update_task()

Description: This method is used to update a 
task's information.

returns: The updated task details.
***********************************************
"""
@tdlapp.put("/tasks/{task_id}")
async def update_task(task_id: int, request: Request, db: Session = Depends(get_db)):
    task_data = await request.json()
    title = task_data.get("title")
    description = task_data.get("description")

    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    if title:
        task.title = title
    if description:
        task.description = description

    db.commit()
    db.refresh(task)
    return task

"""
***********************************************
Method: delete_task()

Description: This method is used to delete a 
task from the database by its ID.

returns: A message indicating the result.
***********************************************
"""
@tdlapp.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()

    task_count = db.query(models.Task).count()
    if task_count == 0:
        db.execute(text("ALTER TABLE tasks AUTO_INCREMENT = 1"))
        db.commit()
        
    return {"detail": "Task deleted"}