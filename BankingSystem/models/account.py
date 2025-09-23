from __future__ import annotations

from typing import Optional
from db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Boolean, ForeignKey
class Account(Base):
    __tablename__ = "accounts"

    account_id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, autoincrement=True)
    amount_decimal: Mapped[int] = mapped_column(Integer, nullable=False)
    is_frozen: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    client_id: Mapped[Optional[int]] = mapped_column(ForeignKey("clients.client_id"))
    client: Mapped["Client"] = relationship(back_populates="accounts")