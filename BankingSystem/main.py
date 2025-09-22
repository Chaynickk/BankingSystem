from fastapi import FastAPI

app = FastAPI(
    title="Banking API",
    version="1.0"
)

@app.get("/ping")
def ping():
    return {"pong": True}