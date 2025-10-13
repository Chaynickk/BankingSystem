import jwt
from fastapi import APIRouter
from fastapi.params import Depends
from config import SECRET_KEY, ALGORITHM
from fastapi.exceptions import HTTPException
from datetime import datetime, timezone, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from crud.admin import registration_admin
from schemes.admin import AdminRegistration

admin_router = APIRouter(prefix="/admin", tags=["Admin"])

admin_jwt = OAuth2PasswordBearer(tokenUrl="/client/login")


def create_jwt_token(client):
    now = datetime.now(timezone.utc)
    payload = {"sub": str(client.client_id),
               "role": "admin",
               "iat": int(now.timestamp()),
               "exp": int((now + timedelta(minutes=20)).timestamp())}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def verification_admin_token(token = Depends(admin_jwt)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload["role"] != "admin":
            raise HTTPException(
                headers={"WWW-Authenticate": "Bearer"},
                status_code=401,
                detail="token error"
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
    admin = await check_logint(admin_login)
    token = create_jwt_token(admin)
    return {"access_token": token, "token_type": "bearer", "admin": admin}

@admin_router.post("/registration")
async def admin_create(admin_data: AdminRegistration):
    admin = await registration_admin(admin_data)
    token = create_jwt_token(admin)
    return {"access_token": token, "token_type": "bearer", "admin": admin}

@admin_router.put("/frieze_account")
def admin_frieze_account():
    pass

@admin_router.get("/get_clients")
def admin_get_clients():
    pass

@admin_router.get("/get_accounts")
def admin_get_accounts():
    pass