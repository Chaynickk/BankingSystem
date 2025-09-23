from db.database import get_session
import asyncio

from models import Account, Admin
from models.client import Client
import models

async def add_user():
    client = Client(
        first_name='12',
        last_name='1234',
        phone_number='12',
        email="14"
    )

    account = Account(
        client_id=2,
        amount_decimal=0
    )

    admin = Admin(
        first_name='12',
        last_name='1234',
        password_hash="124354346gh"
    )


    async with get_session() as session:
        session.add(client)
        session.add(account)
        session.add(admin)
        await session.commit()

asyncio.run(add_user())

