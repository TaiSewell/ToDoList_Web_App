from fastapi import FastAPI
from Database import engine
from Database import Base  # Import Base from models

tdlapp = FastAPI()

Base.metadata.create_all(bind=engine)

@tdlapp.get("/")
def read_root():
    return {"Hello": "World"}

@tdlapp.get("/lists/{list_id}")
def read_list(list_id: int, q: str = None):
    return {"list_id": list_id, "q": q}



