from fastapi import FastAPI
from .routers import acidentes

app = FastAPI()

app.include_router(acidentes.router)

@app.get("/")
def root():
    return {}