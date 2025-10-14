import jwt
from fastapi import APIRouter
from fastapi.params import Depends
from config import SECRET_KEY, ALGORITHM
from fastapi.exceptions import HTTPException
from datetime import datetime, timezone, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from crud.admin import registration_admin, check_login, get_admin_by_id, activate_admin_crud, frieze_account, \
    get_not_activate_admins_crud, select_clients, get_accounts
from schemes.admin import AdminRegistration, SelectClients

admin_router = APIRouter(prefix="/admin", tags=["Admin"])

admin_jwt = OAuth2PasswordBearer(tokenUrl="/admin/login")


def create_jwt_token(admin):
    now = datetime.now(timezone.utc)
    payload = {"sub": str(admin.admin_id),
               "role": "admin",
               "iat": int(now.timestamp()),
               "exp": int((now + timedelta(minutes=20)).timestamp())}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

async def verification_admin_token(token = Depends(admin_jwt)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        admin = await get_admin_by_id(int(payload["sub"]))
        if payload["role"] != "admin":
            raise HTTPException(
                headers={"WWW-Authenticate": "Bearer"},
                status_code=403,
                detail="Don't have enough rights"
            )
        elif admin.is_active is False:
            raise HTTPException(
                headers={"WWW-Authenticate": "Bearer"},
                status_code=403,
                detail="Don't have enough rights"
            )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            headers={"WWW-Authenticate": "Bearer"},
            status_code=401,
            detail="expired token"
        )
    except jwt.InvalidSignatureError:
        raise HTTPException(
            headers={"WWW-Authenticate": "Bearer"},
            status_code=401,
            detail="invalid token signature"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            headers={"WWW-Authenticate": "Bearer"},
            status_code=401,
            detail="token error"
        )

@admin_router.post("/login")
async def admin_logint(admin_login: OAuth2PasswordRequestForm = Depends()):
    admin = await check_login(admin_login)
    token = create_jwt_token(admin)
    return {"access_token": token, "token_type": "bearer", "admin": admin}

@admin_router.post("/registration")
async def admin_create(admin_data: AdminRegistration):
    admin = await registration_admin(admin_data)
    token = create_jwt_token(admin)
    return {"access_token": token, "token_type": "bearer", "admin": admin}

@admin_router.put("/frieze_account")
async def admin_frieze_account(account_id: int, token = Depends(verification_admin_token)):
    account = await frieze_account(account_id)
    return account


@admin_router.put("/activate_admin")
async def activate_admin(admin_id: int, token = Depends(verification_admin_token)):
    admin = await activate_admin_crud(admin_id)
    return admin

@admin_router.delete("/reject_admin")
async def reject_admin(admin_id):
    pass

@admin_router.get("/get_not_activate_admins")
async def get_not_activate_admins():
    admins = await get_not_activate_admins_crud()
    return admins

@admin_router.get("/get_clients")
def admin_get_clients(client_data: SelectClients):
    clients = select_clients(first_name=client_data.first_name,
                             last_name=client_data.last_name,
                             patronymic=client_data.patronymic,
                             email=client_data.email,
                             phone_number=client_data.phone_number,
                             client_id=client_data.client_id)
    return clients

@admin_router.get("/get_accounts")
async def admin_get_accounts(client_id):
    accounts = await get_accounts(client_id)
    return accounts