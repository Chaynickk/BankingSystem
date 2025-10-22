from fastapi import FastAPI
from fastapi.params import Depends

from routes.account import account_router
from routes.admin import admin_router
from routes.client import client_router

app = FastAPI(
    title="Banking API",
    version="1.0"
)


#app.include_router(client_router)
app.include_router(admin_router)
#app.include_router(account_router)

