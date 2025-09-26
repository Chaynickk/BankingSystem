from fastapi.security import OAuth2PasswordRequestForm

from db.database import get_session
from models import Password
from models.client import Client
from schemes.client import ClientRegistration, ClientLogin
from argon2.exceptions import VerifyMismatchError
from fastapi import HTTPException, status
from config import password_hasher
from sqlalchemy import select

async def registration_client(client_data: ClientRegistration):
    async with get_session() as session:
        try:
            some_email = await session.execute(select(Client).where(Client.email == client_data.email))
            if some_email.scalar_one_or_none():
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email already registered"
                )

            some_phone = await session.execute(select(Client).where(Client.phone_number == client_data.phone_number))
            if some_phone.scalar_one_or_none():
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Phone number already registered"
                )

            client = Client(
                first_name=client_data.first_name,
                last_name=client_data.last_name,
                patronymic=client_data.patronymic,
                email=client_data.email,
                phone_number=client_data.phone_number
            )


            session.add(client)
            await session.flush()

            session.add(Password(
                password=password_hasher.hash(client_data.password),
                client_id=client.client_id))
            await session.commit()
            await session.refresh(client)
            return client
        except:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Bad request"
            )

async def check_logint(client_logint: OAuth2PasswordRequestForm):
    async with get_session() as session:
        client = await session.execute(select(Client).where(Client.email == client_logint.username))
        client = client.scalar_one_or_none()
        if client is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={"WWW-Authenticate": "Bearer"}
            )
        result = await session.execute(select(Password.password).where(Password.client_id == client.client_id))
        hash_password = result.scalar_one_or_none()

        try:
            password_hasher.verify(hash_password, client_logint.password)
            return client
        except VerifyMismatchError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={"WWW-Authenticate": "Bearer"}
            )



