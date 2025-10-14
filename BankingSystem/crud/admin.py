from fastapi.security import OAuth2PasswordRequestForm
from argon2.exceptions import VerifyMismatchError
from schemes.admin import AdminRegistration
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from db.database import get_session
from config import password_hasher
from sqlalchemy import select
from models import Admin, Account, Client


async def registration_admin(admin_data: AdminRegistration):
    async with get_session() as session:
        try:
            some_email = await session.execute(select(Admin).where(Admin.email == admin_data.email))
            if some_email.scalar_one_or_none():
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email already registered"
                )

            some_phone = await session.execute(select(Admin).where(Admin.phone_number == admin_data.phone_number))
            if some_phone.scalar_one_or_none():
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Phone number already registered"
                )

            new_admin = Admin(
                first_name = admin_data.first_name,
                last_name = admin_data.last_name,
                patronymic = admin_data.patronymic,
                password_hash = password_hasher.hash(admin_data.password),
                email = admin_data.email,
            )

            await session.commit()
            return new_admin

        except HTTPException as e:
            await session.rollback()
            raise e

        except SQLAlchemyError:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error"
            )

        except Exception as e:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"{e}"
            )

async def check_login(admin_login: OAuth2PasswordRequestForm):
    async with get_session() as session:
        admin = await session.execute(select(Admin).where(Admin.email == admin_login.username))
        admin = admin.scalar_one_or_none()
        if admin is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={"WWW-Authenticate": "Bearer"}
            )

        hash_password = admin.password_hash

        try:
            password_hasher.verify(hash_password, admin_login.password)
            return admin
        except VerifyMismatchError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={"WWW-Authenticate": "Bearer"}
            )

async def activate_admin_crud(admin_id: int):
    async with get_session() as session:
        try:
            admin = await session.execute(Admin).where(Admin.admin_id == admin_id)
            admin = admin.scalar_one_or_none()

            if admin is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Admin is not found"
                )

            admin.is_active = True

            await session.commit()
            return admin
        except HTTPException as e:
            await session.rollback()
            raise e
        except Exception:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

async def get_admin_by_id(admin_id):
    async with get_session() as session:
        try:
            admin = await session.execute(select(Admin).where(Admin.admin_id == admin_id))
            admin = admin.scalar_one_or_none()

            if admin is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Admin is not found"
                )
            return admin
        except HTTPException as e:
            await session.rollback()
            raise e
        except Exception:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

async def frieze_account(account_id):
    async with get_session() as session:
        try:
            account = session.execute(select (Account).where(Account.account_id == account_id))
            account = account.scalar_one_or_none()

            if account is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Account is not found"
                )
            return account
        except HTTPException as e:
            await session.rollback()
            raise e
        except Exception:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

async def get_not_activate_admins_crud():
    async with get_session() as session:
        try:
            admins = session.execute(select (Admin).where(Admin.is_active == False))
            return admins.scalars().all()
        except Exception:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

async def select_clients(client_id: int = None,
                         first_name: str = None,
                         last_name: str = None,
                         patronymic: str = None,
                         phone_number: str = None,
                         email: str = None):
    async with get_session() as session:
        try:
            filters = (client_id, first_name, last_name, patronymic, phone_number, email)

            if not any(filters):
                raise HTTPException

            query = select(Client)

            if client_id is not None:
                query.where(Client.client_id == client_id)

            if first_name is not None:
                query.where(Client.first_name == first_name)

            if last_name is not None:
                query.where(Client.last_name == last_name)

            if patronymic is not None:
                query.where(Client.phone_number == patronymic)

            if phone_number is not None:
                query.where(Client.phone_number == phone_number)

            if email is not None:
                query.where(Client.email == email)

            return await session.scalars(query).all()
        except Exception:
            await session.rollback()
            raise HTTPException(
                status_code=500
            )

async def get_accounts(client_id):
    async with get_session() as session:
        try:
            accounts = await session.execute(select(Account).where(Account.client_id==client_id))
            return accounts.scalars().all()
        except Exception:
            await session.rollback()
            raise HTTPException(
                status_code=500
            )

async def reject_admin_crud(admin_id):
    async with get_session() as session:
        try:
            result = await session.execute(select(Admin).where(Admin.admin_id == admin_id))
            admin = result.scalar_one_or_none()

            if admin is None:
                raise HTTPException(
                    status_code=404,
                    detail="Admin is not found"
                )
            if admin.is_active:
                raise HTTPException(
                    status_code=403,
                    detail="Not enough rights"
                )

            await session.delete(admin)
            await session.commit()
        except HTTPException as e:
            session.rollback()
            raise e
        except Exception:
            await session.rollback()
            raise HTTPException(
                status_code=500
            )
