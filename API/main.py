from fastapi import FastAPI
from pydantic import BaseModel, Field
from uuid import UUID



tdlApp = FastAPI()

class Task(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)

TASKS = []

@tdlApp.get("/")
def read_api():
    return TASKS


tdlApp.post("/")
def create_task(task: Task):
    TASKS.append(task)
    return task
