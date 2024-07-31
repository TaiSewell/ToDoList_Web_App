from fastapi import FastAPI

tdlapp = FastAPI()

@tdlapp.get("/")
def read_root():
    return {"message": "Hello, Tai!!"}