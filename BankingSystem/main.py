from fastapi import FastAPI
from fastapi.params import Depends

from routes.account import account_router
from routes.client import client_router, verification_client_token

app = FastAPI(
    title="Banking API",
    version="1.0"
)

app.include_router(client_router)
app.include_router(account_router)

@app.get("/ping")
def ping(token = Depends(verification_client_token)):
    return {"pong": token}