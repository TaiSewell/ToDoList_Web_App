"""
***********************************************
Developer: Tai Sewell

File: tasks.py

Description: File that contains task-related endpoints.
***********************************************
"""
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import text
from sqlalchemy.orm import Session
from Database.src import database, models
from ..auth import hash_password, verify_password, create_access_token, decode_access_token, get_current_user

# Create a router
router = APIRouter()

# Import get_db function
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


"""
***********************************************
           All Task Endpoints/Methods
***********************************************
***********************************************
Method: create_task()

Description: This method is used to create a task
for the authenticated user.

returns: The created task object.
***********************************************
"""
@router.post("/tasks/")
async def create_task(request: Request, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    task_data = await request.json()
    title = task_data.get("title")
    description = task_data.get("description")

    # Create a new task and associate it with the current user
    new_task = models.Task(title=title, description=description, owner_id=current_user.id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

"""
***********************************************
Method: read_tasks()

Description: This method is used to fetch all 
tasks for the authenticated user.

returns: A list of tasks.
***********************************************
"""
@router.get("/tasks/")
def read_tasks(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    tasks = db.query(models.Task).filter(models.Task.owner_id == current_user.id).all()
    return tasks

"""
***********************************************
Method: read_task()

Description: This method is used to retrieve a task
based on the task_id for the authenticated user.

returns: A task object.
***********************************************
"""
@router.get("/tasks/{task_id}")
def read_task(task_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.owner_id == current_user.id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found or access denied")
    return task

"""
***********************************************
Method: update_task()

Description: This method is used to update a task's
information for the authenticated user.

returns: The updated task details.
***********************************************
"""
@router.put("/tasks/{task_id}")
async def update_task(task_id: int, request: Request, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    task_data = await request.json()
    title = task_data.get("title")
    description = task_data.get("description")

    task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.owner_id == current_user.id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found or access denied")

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

Description: This method is used to delete a task
from the database by its ID for the authenticated user.

returns: A message indicating the result.
***********************************************
"""
@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.owner_id == current_user.id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found or access denied")

    db.delete(task)
    db.commit()

    task_count = db.query(models.Task).filter(models.Task.owner_id == current_user.id).count()
    if task_count == 0:
        db.execute(text("ALTER TABLE tasks AUTO_INCREMENT = 1"))
        db.commit()
        
    return {"detail": "Task deleted"}
