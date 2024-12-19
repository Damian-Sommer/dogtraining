import uuid
from enum import StrEnum
from typing import List

import attrs
from sqlalchemy import exc, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import selectinload

from server.models import Card, Training


class TrainingType(StrEnum):
    UNTERORDNUNGSSPAZIERGANG = "unterordnungsspaziergang"
    QUERBEET = "querbeet"
    ALLTAGSSPAZIERGANG = "alltagsspaziergang"


@attrs.define
class TrainingSpec:
    timestamp: int = attrs.field()
    type: TrainingType = attrs.field()
    dogs: List[str] = attrs.field()
    card_id: str = attrs.field()

    @type.validator
    def check_type(self, attribute, value):
        if value not in list(TrainingType):
            raise TrainingSpecInvalid(
                f"The training type: {value}, is invalid, please use one of the valid types: {[v.value for v in TrainingType]}"
            )

    @timestamp.validator
    def check_timestamp(self, attribute, value):
        if not isinstance(value, int) or value <= 0:
            raise TrainingSpecInvalid(
                f"The timestamp of a training can not be below 0 and has to be of the type int but was: {value} and of type: {type(value)}",
            )

    @dogs.validator
    def check_dogs(self, attribute, value):
        if (
            not isinstance(value, list)
            or len(value) == 0
            or not all(isinstance(item, str) for item in value)
        ):
            raise TrainingSpecInvalid(
                f"The dogs of a training have to be of type: List[str], but was: {type(value)}",
            )

    @card_id.validator
    def check_card_id(self, attribute, value):
        if not isinstance(value, str):
            raise TrainingSpecInvalid(
                f"The card_id of a training has to be of type str but was: {value} and of type: {type(value)}",
            )

    @classmethod
    def from_json(cls, *, data):
        keys = ["timestamp", "type", "dogs", "card_id"]
        for k in keys:
            if k not in data:
                raise InvalidPayload(
                    f"You have to provide a payload with the following keys: {keys}"
                )
        return cls(
            timestamp=data["timestamp"],
            type=data["type"],
            dogs=data["dogs"],
            card_id=data["card_id"],
        )


@attrs.define
class CardSpec:
    timestamp: int = attrs.field()
    slots: int = attrs.field()
    cost: int = attrs.field()

    @timestamp.validator
    def check_timestamp(self, attribute, value):
        if not isinstance(value, int) or value <= 0:
            raise CardSpecInvalid(
                f"The timestamp of a card can not be below 0 and has to be of the type int but was: {value} and of type: {type(value)}",
            )

    @cost.validator
    def check_cost(self, attribute, value):
        if not isinstance(value, int) or value <= 0:
            raise CardSpecInvalid(
                f"The cost of a card can not be below 0 and has to be of the type int but was: {value} and of type: {type(value)}",
            )

    @slots.validator
    def check_slots(self, attribute, value):
        if not isinstance(value, int) or value <= 0:
            raise CardSpecInvalid(
                f"The slots of a card can not be below 0 and has to be of the type int but was: {value} and of type: {type(value)}",
            )

    @classmethod
    def from_json(cls, *, data):
        for k in ["timestamp", "cost", "slots"]:
            if k not in data:
                raise InvalidPayload(
                    f"You have to provide a payload with the following keys: {["timestamp", "cost", "slots"]}"
                )
        return cls(
            timestamp=data["timestamp"],
            cost=data["cost"],
            slots=data["slots"],
        )


class TrainingDatabase:
    def __init__(self, connection):
        engine = create_async_engine(connection)
        self.async_session = async_sessionmaker(engine, expire_on_commit=False)

    async def create_training_entry(self, *, training_spec) -> List[Training]:
        async with self.async_session() as session:
            async with session.begin():
                try:
                    card = await session.execute(
                        select(Card).where(Card.id == training_spec.card_id)
                    )
                    card.scalars().one()
                except exc.NoResultFound:
                    raise CardNotFound(
                        f"There is no card with the specified card_id: {training_spec.card_id}"
                    )
                trainings: List[Training] = [
                    Training(
                        id=str(uuid.uuid4()),
                        timestamp=training_spec.timestamp,
                        type=str(training_spec.type),
                        dog=dog,
                        card_id=training_spec.card_id,
                    )
                    for dog in training_spec.dogs
                ]
                session.add_all(trainings)
                await session.flush()
                await session.commit()
                return trainings

    async def get_training_entry_by_id(self, *, training_id) -> Training:
        async with self.async_session() as session:
            async with session.begin():
                try:
                    result = await session.execute(
                        select(Training)
                        .where(Training.id == training_id)
                        .options(selectinload(Training.card))
                    )
                    return result.scalars().one()
                except NoResultFound:
                    raise TrainingNotFound(
                        f"The requested training entry with id: {training_id} does not exist"
                    )

    async def get_all_training_entries(self) -> List[Training]:
        async with self.async_session() as session:
            async with session.begin():
                result = await session.execute(
                    select(Training).options(selectinload(Training.card))
                )
                return result.scalars().all()

    async def create_card_entry(self, *, card_spec: CardSpec) -> Card:
        async with self.async_session() as session:
            async with session.begin():
                card = Card(
                    id=str(uuid.uuid4()),
                    timestamp=card_spec.timestamp,
                    cost=card_spec.cost,
                    slots=card_spec.slots,
                )
                session.add(card)
                await session.flush()
                await session.commit()
                return card

    async def get_card_entry_by_id(self, *, card_id) -> Card:
        async with self.async_session() as session:
            async with session.begin():
                try:
                    result = await session.execute(
                        select(Card)
                        .where(Card.id == card_id)
                        .options(selectinload(Card.trainings))
                    )
                    return result.scalars().one()
                except NoResultFound:
                    raise CardNotFound(
                        f"The requested card entry with id: {card_id} does not exist"
                    )

    async def get_all_card_entries(self) -> List[Card]:
        async with self.async_session() as session:
            async with session.begin():
                result = await session.execute(
                    select(Card).options(selectinload(Card.trainings))
                )
                return result.scalars().all()


class TrainingSpecInvalid(Exception):
    pass


class DatabaseException(Exception):
    pass


class TrainingNotFound(DatabaseException):
    pass


class CardNotFound(DatabaseException):
    pass


class CardSpecInvalid(Exception):
    pass


class InvalidPayload(Exception):
    pass
