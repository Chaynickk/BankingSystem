from __future__ import annotations
from db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Boolean,String, DateTime, func, Text, ForeignKey
from typing import Optional

class Password(Base):
    __tablename__ = "clients_passwords"

    password: Mapped[str] = mapped_column(Text, nullable=False)

    client_id: Mapped[int] = mapped_column(ForeignKey("clients.client_id"), primary_key=True, nullable=False)
    client: Mapped["Client"] = relationship("Client", back_populates="clients_passwords")

