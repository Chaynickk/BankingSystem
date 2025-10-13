from config import password_hasher
from models import Admin
from schemes.admin import AdminRegistration
from sqlalchemy.exc import SQLAlchemyError
from db.database import get_session
from fastapi import HTTPException, status
from sqlalchemy import select

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

async def check_logint(admin_login):
    pass