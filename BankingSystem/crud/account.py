from sqlalchemy.exc import SQLAlchemyError

from config import MAX_BALANCE
from db.database import get_session
from models import Account
from fastapi import HTTPException, status
from sqlalchemy import select

from schemes.account import Transaction


async def select_account(client_id: int):
    async with get_session() as session:
        try:
            res = await session.execute(select(Account).where(Account.client_id == client_id))
            return res.scalars().all()
        except Exception as e:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"{e}"
            )

async def create_account(client_id:int):
    async with get_session() as session:
        try:
            new_account = Account(
                amount_decimal = 0,
                is_frozen = False,
                client_id = client_id
            )

            session.add(new_account)
            await session.commit()
            await session.refresh(new_account)

            return new_account
        except:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error"
            )

async def disconnect_client_from_account(client_id: int, account_id: int):
    async with get_session() as session:
        try:
            res = await session.execute(select(Account).where((Account.client_id == client_id) & (Account.account_id == account_id)))
            account = res.scalar_one_or_none()

            if account is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Account not found",
                )

            account.client_id = None

            await session.commit()
            await session.refresh(account)

            return account
        except:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error"
            )

async def completion_transaction(client_id: int, transaction: Transaction):
    async with get_session() as session:
        try:
            res = await session.execute(select(Account).where((Account.client_id == client_id) & (Account.account_id == transaction.from_account_id)))
            if res.scalar_one_or_none() is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"The client doesn’t own the account"
                )

            result = await session.execute(
                select(Account)
                .where(Account.account_id.in_([transaction.from_account_id, transaction.to_account_id]))
                .with_for_update()
            )
            accounts = {acc.account_id: acc for acc in result.scalars().all()}

            from_account = accounts.get(transaction.from_account_id)
            to_account = accounts.get(transaction.to_account_id)

            if from_account is None or to_account is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Account not found"
                )

            if from_account.amount_decimal - transaction.money < 0:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Not enough balance to complete the transaction"
                )

            if to_account.amount_decimal + transaction.money > MAX_BALANCE:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Destination account balance limit would be exceeded {to_account.amount_decimal, transaction.money}"
                )

            if from_account.is_frozen or to_account.is_frozen:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Account is freeze"
                )

            if transaction.money is None or transaction.money <= 0:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Amount must be greater than zero"
                )

            from_account.amount_decimal -= transaction.money
            to_account.amount_decimal += transaction.money

            await session.commit()


        except HTTPException as e:
            await session.rollback()
            raise e

        except SQLAlchemyError:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error"
            )

        except Exception:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )
