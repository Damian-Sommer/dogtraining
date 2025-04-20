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
    user_id: Mapped[str] = mapped_column(String, nullable=False)

    card_id = mapped_column(String, ForeignKey("card.id"), nullable=False)
    dog_id = mapped_column(String, ForeignKey("dog.id"), nullable=False)

    card = relationship("Card", uselist=False, back_populates="trainings")
    dog = relationship("Dog", uselist=False, back_populates="trainings")

    def as_dict(self):
        return dict(
            id=self.id,
            timestamp=self.timestamp,
            type=self.type,
            dog_id=self.dog_id,
            card_id=self.card_id,
            user_id=self.user_id,
        )


class Card(Base):
    __tablename__ = "card"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, unique=True, nullable=False
    )
    timestamp: Mapped[int] = mapped_column(Integer, nullable=False)
    cost: Mapped[int] = mapped_column(Integer, nullable=False)
    slots: Mapped[int] = mapped_column(Integer, nullable=False)
    user_id: Mapped[str] = mapped_column(String, nullable=False)

    trainings = relationship("Training", back_populates="card")

    def as_dict(self):
        return dict(
            id=self.id,
            timestamp=self.timestamp,
            cost=self.cost,
            slots=self.slots,
            user_id=self.user_id,
        )


class Dog(Base):
    __tablename__ = "dog"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, unique=True, nullable=False
    )
    registration_time: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[str] = mapped_column(String, nullable=False)

    trainings = relationship("Training", back_populates="dog")

    def as_dict(self):
        return dict(
            id=self.id,
            registration_time=self.registration_time,
            name=self.name,
            user_id=self.user_id,
        )
