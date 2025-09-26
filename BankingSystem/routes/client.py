from datetime import datetime, timezone, timedelta

from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException
from config import SECRET_KEY, ALGORITHM
from crud.client import registration_client, check_logint
from schemes.client import ClientRegistration
import jwt

client_router = APIRouter(prefix="/client", tags=["Client"])

client_jwt = OAuth2PasswordBearer(tokenUrl="/client/login")

def create_jwt_token(client):
    now = datetime.now(timezone.utc)
    payload = {"sub": str(client.client_id),
               "role": "client",
               "iat": int(now.timestamp()),
               "exp": int((now + timedelta(minutes=20)).timestamp())}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verification_client_token(token = Depends(client_jwt)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
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

@client_router.post("/registration")
async def client_create(client_data: ClientRegistration):
    client = await registration_client(client_data)
    token = create_jwt_token(client)
    return {"access_token": token, "token_type": "bearer"}

@client_router.post("/login")
async def client_logint(client_login: OAuth2PasswordRequestForm = Depends()):
    client = await check_logint(client_login)
    token = create_jwt_token(client)
    return {"access_token": token, "token_type": "bearer"}



