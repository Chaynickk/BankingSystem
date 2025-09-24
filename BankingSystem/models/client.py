from __future__ import annotations
from db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Boolean,String, DateTime, func
from typing import Optional, List
from datetime import datetime
class Client(Base):
    __tablename__ = "clients"

    client_id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(75), nullable=False)
    last_name: Mapped[str] = mapped_column(String(75), nullable=False)
    patronymic: Mapped[Optional[str]] = mapped_column(String(75))
    phone_number: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(320), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    accounts: Mapped[List["Account"]] = relationship("Account", back_populates="client")
    clients_passwords: Mapped["Password"] = relationship("Password", back_populates="client", uselist=False)

