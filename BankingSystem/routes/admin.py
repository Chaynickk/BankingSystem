from fastapi import APIRouter

admin_router = APIRouter(prefix="/admin", tags=["Admin"])

@admin_router.post("/login")
def admin_logint():
    pass

@admin_router.post("/registration")
def admin_create():
    pass

@admin_router.put("/frieze_account")
def admin_frieze_account():
    pass

@admin_router.get("/get_clients")
def admin_get_clients():
    pass

@admin_router.get("/get_accounts")
def admin_get_accounts():
    pass