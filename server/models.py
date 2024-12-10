from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


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
    card_id = mapped_column(String, ForeignKey("card.id"), nullable=False)

    card = relationship("Card", uselist=False, back_populates="trainings")


class Card(Base):
    __tablename__ = "card"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, unique=True, nullable=False
    )
    timestamp: Mapped[int] = mapped_column(Integer, nullable=False)
    cost: Mapped[int] = mapped_column(Integer, nullable=False)
    slots: Mapped[int] = mapped_column(Integer, nullable=False)

    trainings = relationship("Training", back_populates="card")
