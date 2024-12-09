from sqlalchemy import Integer, String
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Training(Base):
    __tablename__ = "training"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, unique=True, nullable=False
    )
    timestamp: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False)
    used_slots: Mapped[int] = mapped_column(Integer, nullable=False)


class Card(Base):
    __tablename__ = "card"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, unique=True, nullable=False
    )
    timestamp: Mapped[int] = mapped_column(Integer, nullable=False)
    cost: Mapped[int] = mapped_column(Integer, nullable=False)
    slots: Mapped[int] = mapped_column(Integer, nullable=False)
