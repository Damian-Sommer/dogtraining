import re

import pytest
from sqlalchemy.ext.asyncio import create_async_engine

from server.models import Base, Training
from server.training_database import (
    TrainingDatabase,
    TrainingNotFound,
    TrainingSpec,
    TrainingSpecInvalid,
    TrainingType,
)


@pytest.fixture
def connection(tmp_path):
    db = tmp_path / "test.db"
    return f"sqlite+aiosqlite:///{db}"


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
def training_timestamp():
    return 1


@pytest.fixture
def training_used_slots():
    return 1


@pytest.fixture
def training_type():
    return TrainingType.ALLTAGSSPAZIERGANG


async def test_create_training_entry_fails_because_of_invalid_type(
    training_timestamp,
    training_used_slots,
):
    training_type = "some-type"

    with pytest.raises(
        TrainingSpecInvalid,
        match=re.escape(
            f"The training type: {training_type}, is invalid,"
            f" please use one of the valid types: {[v.value for v in TrainingType]}"
        ),
    ):
        TrainingSpec(
            timestamp=training_timestamp,
            type=training_type,
            used_slots=training_used_slots,
        )


@pytest.mark.parametrize(
    "training_timestamp",
    [
        -1,
        0,
        1e3,
        "some string",
        list(),
        set(),
        dict(),
    ],
)
async def test_create_training_entry_fails_because_of_invalid_date_timestamp(
    training_database, training_type, training_used_slots, training_timestamp
):
    with pytest.raises(
        TrainingSpecInvalid,
        match=re.escape(
            f"The timestamp of a training can not be below 0 and"
            f" has to be of the type int but was: {training_timestamp}"
            f" and of type: {type(training_timestamp)}",
        ),
    ):
        TrainingSpec(
            timestamp=training_timestamp,
            type=training_type,
            used_slots=training_used_slots,
        )


@pytest.mark.parametrize(
    "used_slots",
    [
        -1,
        0,
        1e3,
        "some string",
        list(),
        set(),
        dict(),
    ],
)
async def test_create_training_entry_fails_because_of_invalid_used_slots(
    training_type, training_timestamp, used_slots
):
    with pytest.raises(
        TrainingSpecInvalid,
        match=re.escape(
            f"The used_slots of a training can not be below 0 and"
            f" has to be of the type int but was: {used_slots}"
            f" and of type: {type(used_slots)}",
        ),
    ):
        TrainingSpec(
            timestamp=training_timestamp,
            type=training_type,
            used_slots=used_slots,
        )


@pytest.mark.parametrize(
    "training_type",
    [
        TrainingType.ALLTAGSSPAZIERGANG,
        TrainingType.QUERBEET,
        TrainingType.UNTERORDNUNGSSPAZIERGANG,
    ],
)
async def test_create_training_entry_with_valid_data_succeeds(
    training_database,
    training_type,
    training_timestamp,
    training_used_slots,
):
    await training_database.create_training_entry(
        training_spec=TrainingSpec(
            timestamp=training_timestamp,
            type=training_type,
            used_slots=training_used_slots,
        )
    )


async def test_get_training_entry_by_id(
    training_database,
    training_timestamp,
    training_type,
    training_used_slots,
):
    training = await training_database.create_training_entry(
        training_spec=TrainingSpec(
            timestamp=training_timestamp,
            type=training_type,
            used_slots=training_used_slots,
        )
    )

    actual_training: Training = await training_database.get_training_entry_by_id(
        training_id=training.id
    )
    assert actual_training.timestamp == training_timestamp
    assert actual_training.type == training_type
    assert actual_training.used_slots == training_used_slots


async def test_get_training_entry_by_id_fails_if_not_existing(training_database):
    training_id = "some-id"
    with pytest.raises(
        TrainingNotFound,
        match=f"The requested training entry with id: {training_id} does not exist",
    ):
        await training_database.get_training_entry_by_id(training_id=training_id)


async def test_get_all_training_entries(training_database, training_type):
    training_specs = [
        TrainingSpec(
            timestamp=i + 1,
            type=training_type,
            used_slots=i + 1,
        )
        for i in range(4)
    ]
    for training_spec in training_specs:
        await training_database.create_training_entry(training_spec=training_spec)

    trainings = await training_database.get_all_training_entries()

    assert len(trainings) == 4


async def test_get_all_trainings_but_not_training_exists(training_database):
    trainings = await training_database.get_all_training_entries()
    assert not trainings
