from fastapi import APIRouter
from fastapi.params import Depends

from crud.account import select_account
from .client import verification_client_token

account_router = APIRouter(prefix="/account", tags=["Account"])

@account_router.post("/registration")
async def account_create(token=Depends(verification_client_token)):
    pass

@account_router.get("/get")
async def accounts_get(token=Depends(verification_client_token)):
    accounts = await select_account(token["sub"])
    return accounts

@account_router.delete("/del")
async def account_del(token=Depends(verification_client_token)):
    pass

@account_router.put("/transaction")
async def account_transaction(token=Depends(verification_client_token)):
    pass