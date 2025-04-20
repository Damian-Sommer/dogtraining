import uuid
from enum import StrEnum
from typing import List

import attrs
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import selectinload

from dogtraining.server.models import Card, Dog, Training


class TrainingType(StrEnum):
    UNTERORDNUNGSSPAZIERGANG = "unterordnungsspaziergang"
    QUERBEET = "querbeet"
    ALLTAGSSPAZIERGANG = "alltagsspaziergang"


@attrs.define
class TrainingSpec:
    timestamp: int = attrs.field()
    type: TrainingType = attrs.field()
    dogs: List[str] = attrs.field()
    user_id: str = attrs.field()

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

    @user_id.validator
    def check_user_id(self, attribute, value):
        if not isinstance(value, str):
            raise TrainingSpecInvalid(
                f"The user_id of a training has to be of type str but was: {value} and of type: {type(value)}",
            )

    @classmethod
    def from_json(cls, *, data, user_id):
        keys = ["timestamp", "type", "dogs"]
        for k in keys:
            if k not in data:
                raise InvalidPayload(
                    f"You have to provide a payload with the following keys: {keys}"
                )
        return cls(
            timestamp=data["timestamp"],
            type=data["type"],
            dogs=data["dogs"],
            user_id=user_id,
        )


@attrs.define
class CardSpec:
    timestamp: int = attrs.field()
    slots: int = attrs.field()
    cost: int = attrs.field()
    user_id: str = attrs.field()

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

    @user_id.validator
    def check_user_id(self, attribute, value):
        if not isinstance(value, str):
            raise CardSpecInvalid(
                f"The user_id of a card has to be of type str but was: {value} and of type: {type(value)}",
            )

    @classmethod
    def from_json(cls, *, data, user_id):
        keys = ["timestamp", "cost", "slots"]
        for k in keys:
            if k not in data:
                raise InvalidPayload(
                    f"You have to provide a payload with the following keys: {keys}"
                )
        return cls(
            timestamp=data["timestamp"],
            cost=data["cost"],
            slots=data["slots"],
            user_id=user_id,
        )


@attrs.define
class DogSpec:
    registration_time: int = attrs.field()
    name: str = attrs.field()
    user_id: str = attrs.field()

    @registration_time.validator
    def check_registration_time(self, attribute, value):
        if not isinstance(value, int) or value <= 0:
            raise DogSpecInvalid(
                f"The registration_time of a dog can not be below 0 and has to be of the type int but was: {value} and of type: {type(value)}",
            )

    @name.validator
    def check_name(self, attribute, value):
        if not isinstance(value, str):
            raise DogSpecInvalid(
                f"The name of a dog has to be of type str but was: {value} and of type: {type(value)}",
            )

    @user_id.validator
    def check_user_id(self, attribute, value):
        if not isinstance(value, str):
            raise DogSpecInvalid(
                f"The user_id of a dog has to be of type str but was: {value} and of type: {type(value)}",
            )

    @classmethod
    def from_json(cls, *, data, user_id):
        keys = ["registration_time", "name"]
        for k in keys:
            if k not in data:
                raise InvalidPayload(
                    f"You have to provide a payload with the following keys: {keys}"
                )
        return cls(
            registration_time=data["registration_time"],
            name=data["name"],
            user_id=user_id,
        )


class TrainingDatabase:
    def __init__(self, connection):
        engine = create_async_engine(connection)
        self.async_session = async_sessionmaker(engine, expire_on_commit=False)

    async def create_training_entry(
        self, *, training_spec: TrainingSpec
    ) -> List[Training]:
        cards: List[Card] = await self._get_all_free_cards(
            user_id=training_spec.user_id,
        )
        free_slots_per_card = [
            card.id for card in cards for _ in range(card.slots - len(card.trainings))
        ]
        free_slots = len(free_slots_per_card)
        if len(training_spec.dogs) > free_slots:
            raise CardFull(
                f"Only {free_slots} slot available but {len(training_spec.dogs)} amount of slots are required, register a new card first before trying this operation again."
            )
        async with self.async_session() as session:
            async with session.begin():
                trainings: List[Training] = []
                for dog_id in training_spec.dogs:
                    trainings.append(
                        Training(
                            id=str(uuid.uuid4()),
                            timestamp=training_spec.timestamp,
                            type=str(training_spec.type),
                            dog_id=dog_id,
                            card_id=free_slots_per_card.pop(0),
                            user_id=training_spec.user_id,
                        )
                    )
                session.add_all(trainings)
                await session.flush()
                await session.commit()
                return trainings

    async def get_training_entry_by_id(self, *, training_id, user_id) -> Training:
        async with self.async_session() as session:
            async with session.begin():
                try:
                    result = await session.execute(
                        select(Training)
                        .where(Training.user_id == user_id)
                        .where(Training.id == training_id)
                        .options(selectinload(Training.card))
                        .options(selectinload(Training.dog))
                    )
                    return result.scalars().one()
                except NoResultFound:
                    raise TrainingNotFound(
                        f"The requested training entry with id: {training_id} does not exist"
                    )

    async def get_all_training_entries(self, *, user_id) -> List[Training]:
        async with self.async_session() as session:
            async with session.begin():
                result = await session.execute(
                    select(Training)
                    .where(Training.user_id == user_id)
                    .options(selectinload(Training.card))
                    .options(selectinload(Training.dog))
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
                    user_id=card_spec.user_id,
                )
                session.add(card)
                await session.flush()
                await session.commit()
                return card

    async def get_card_entry_by_id(self, *, card_id, user_id) -> Card:
        async with self.async_session() as session:
            async with session.begin():
                try:
                    result = await session.execute(
                        select(Card)
                        .where(Card.user_id == user_id)
                        .where(Card.id == card_id)
                        .options(selectinload(Card.trainings))
                    )
                    return result.scalars().one()
                except NoResultFound:
                    raise CardNotFound(
                        f"The requested card entry with id: {card_id} does not exist"
                    )

    async def get_all_card_entries(self, *, user_id) -> List[Card]:
        async with self.async_session() as session:
            async with session.begin():
                result = await session.execute(
                    select(Card)
                    .where(Card.user_id == user_id)
                    .options(selectinload(Card.trainings))
                )
                return result.scalars().all()

    async def _get_all_free_cards(self, *, user_id) -> List[Card]:
        cards: List[Card] = await self.get_all_card_entries(user_id=user_id)
        return [card for card in cards for _ in range(card.slots - len(card.trainings))]

    async def create_dog_entry(self, *, dog_spec: DogSpec) -> Dog:
        async with self.async_session() as session:
            async with session.begin():
                dog = Dog(
                    id=str(uuid.uuid4()),
                    registration_time=dog_spec.registration_time,
                    name=dog_spec.name,
                    user_id=dog_spec.user_id,
                )
                session.add(dog)
                await session.flush()
                await session.commit()
                return dog

    async def get_dog_by_id(self, *, dog_id, user_id):
        async with self.async_session() as session:
            async with session.begin():
                try:
                    result = await session.execute(
                        select(Dog)
                        .where(Dog.user_id == user_id)
                        .where(Dog.id == dog_id)
                    )
                    return result.scalars().one()
                except NoResultFound:
                    raise DogNotFound(
                        f"The requested dog entry with id: {dog_id} does not exist"
                    )

    async def get_all_dogs(self, *, user_id):
        async with self.async_session() as session:
            async with session.begin():
                result = await session.execute(
                    select(Dog).where(Dog.user_id == user_id)
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


class CardFull(Exception):
    pass


class DogSpecInvalid(Exception):
    pass


class DogNotFound(Exception):
    pass
