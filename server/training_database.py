import uuid
from enum import StrEnum
from typing import List

import attrs
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from server.models import Training


class TrainingType(StrEnum):
    UNTERORDNUNGSSPAZIERGANG = "unterordnungsspaziergang"
    QUERBEET = "querbeet"
    ALLTAGSSPAZIERGANG = "alltagsspaziergang"


@attrs.define
class TrainingSpec:
    timestamp: int = attrs.field()
    type: TrainingType = attrs.field()
    used_slots: int = attrs.field()

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

    @used_slots.validator
    def check_used_slots(self, attribute, value):
        if not isinstance(value, int) or value <= 0:
            raise TrainingSpecInvalid(
                f"The used_slots of a training can not be below 0 and has to be of the type int but was: {value} and of type: {type(value)}",
            )


class TrainingDatabase:
    def __init__(self, connection):
        engine = create_async_engine(connection)
        self.async_session = async_sessionmaker(engine, expire_on_commit=False)

    async def create_training_entry(self, *, training_spec) -> Training:
        async with self.async_session() as session:
            async with session.begin():
                training: Training = Training(
                    id=str(uuid.uuid4()),
                    timestamp=training_spec.timestamp,
                    type=str(training_spec.type),
                    used_slots=training_spec.used_slots,
                )
                session.add(training)
                await session.flush()
                await session.commit()
                return training

    async def get_training_entry_by_id(self, *, training_id) -> Training:
        async with self.async_session() as session:
            async with session.begin():
                try:
                    result = await session.execute(
                        select(Training).where(Training.id == training_id)
                    )
                    return result.scalars().one()
                except NoResultFound:
                    raise TrainingNotFound(
                        f"The requested training entry with id: {training_id} does not exist"
                    )

    async def get_all_training_entries(self) -> List[Training]:
        async with self.async_session() as session:
            async with session.begin():
                result = await session.execute(select(Training))
                return result.scalars().all()


class TrainingSpecInvalid(Exception):
    pass


class DatabaseException(Exception):
    pass


class TrainingNotFound(DatabaseException):
    pass
