from db.database import get_session
from models import Account
from fastapi import HTTPException, status
from sqlalchemy import select

async def select_account(client_id: int):
    async with get_session() as session:
        try:
            res = await session.execute(select(Account).where(Account.client_id == client_id))
            return res.all()
        except:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error"
            )


