from fastapi import APIRouter

account_router = APIRouter(prefix="/account", tags=["Account"])

@account_router.post("/registration")
def account_create():
    pass

@account_router.get("/get")
def account_get():
    pass


@account_router.delete("/del")
def account_del():
    pass

@account_router.put("/transaction")
def account_transaction():
    pass