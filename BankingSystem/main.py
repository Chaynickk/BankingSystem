from fastapi import FastAPI
from routes.client import client_router

app = FastAPI(
    title="Banking API",
    version="1.0"
)

app.include_router(client_router)

@app.get("/ping")
def ping():
    return {"pong": True}