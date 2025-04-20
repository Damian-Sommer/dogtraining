import pytest
from sqlalchemy.ext.asyncio import create_async_engine

from dogtraining.server.models import Base, Card, Dog, Training
from dogtraining.server.training_database import (
    CardSpec,
    DogSpec,
    TrainingDatabase,
    TrainingSpec,
    TrainingType,
)


@pytest.fixture
def training_timestamp():
    return 1


@pytest.fixture
def training_dogs():
    return ["some-dog"]


@pytest.fixture
def training_type():
    return TrainingType.ALLTAGSSPAZIERGANG


@pytest.fixture
def connection(tmp_path):
    db = tmp_path / "test.db"
    return f"sqlite+aiosqlite:///{db}"


@pytest.fixture
def user_id():
    return "thie"


@pytest.fixture
async def init_db(connection):
    engine = create_async_engine(connection)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture
async def training_database(init_db, connection):
    return TrainingDatabase(connection=connection)


@pytest.fixture
def dog_name():
    return "test"


@pytest.fixture
def dog_registration_time():
    return 19


@pytest.fixture
def create_dog_entry(training_database, user_id, dog_name, dog_registration_time):
    async def create_entry() -> Dog:
        return await training_database.create_dog_entry(
            dog_spec=DogSpec(
                registration_time=dog_registration_time,
                name=dog_name,
                user_id=user_id,
            )
        )

    return create_entry


@pytest.fixture
def create_card_entry(training_database: TrainingDatabase, user_id):
    async def create_entry() -> Card:
        return await training_database.create_card_entry(
            card_spec=CardSpec(
                cost=1,
                slots=1,
                timestamp=1,
                user_id=user_id,
            )
        )

    return create_entry


@pytest.fixture
def create_training_entry(
    training_database: TrainingDatabase,
    training_timestamp,
    training_type,
    user_id,
):
    async def create_entry(dogs: list) -> Training:
        return await training_database.create_training_entry(
            training_spec=TrainingSpec(
                timestamp=training_timestamp,
                type=training_type,
                dogs=dogs,
                user_id=user_id,
            )
        )

    return create_entry
