from fastapi import FastAPI

tdlapp = FastAPI()

@tdlapp.get("/")
def read_root():
    return {"Hello": "World"}

@tdlapp.get("/lists/{list_id}")
def read_list(list_id: int, q: str = None):
    return {"list_id": list_id, "q": q}



