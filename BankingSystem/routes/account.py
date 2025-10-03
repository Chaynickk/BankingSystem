from fastapi import APIRouter
from fastapi.params import Depends

from crud.account import select_account, create_account, disconnect_client_from_account, completion_transaction
from schemes.account import Transaction
from .client import verification_client_token

account_router = APIRouter(prefix="/account", tags=["Account"])

@account_router.post("/registration")
async def account_registration(token=Depends(verification_client_token)):
    new_account = await create_account(int(token["sub"]))
    return {"Create": new_account}

@account_router.get("/get")
async def accounts_get(token=Depends(verification_client_token)):
    print("ROUTER")
    accounts = await select_account(int(token["sub"]))
    return {"Accounts": accounts}

@account_router.delete("/del")
async def account_del(account_id: int, token=Depends(verification_client_token)):
    await disconnect_client_from_account(client_id=int(token["sub"]), account_id=account_id)
    return {"Del": True}

@account_router.put("/transaction")
async def account_transaction(transaction: Transaction, token=Depends(verification_client_token)):
    await completion_transaction(client_id=int(token["sub"]), transaction=transaction)
    return {"ok": True}