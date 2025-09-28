from pydantic import BaseModel

class Transaction(BaseModel):
    from_account_id: int
    to_account_id: int
    money: int
