"""
***********************************************
Developer: Tai Sewell

File: tasks.py

Description: File that contains all task related
endpoints/routes.
***********************************************
"""

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