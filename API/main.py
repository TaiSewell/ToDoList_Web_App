from fastapi import FastAPI

tdlApp = FastAPI()


@tdlApp.get("/")
def read_api():
    return {'Home': 'Page'}
