import pytest
from sqlalchemy.ext.asyncio import create_async_engine

from server.models import Base, Card, Training
from server.training_database import (
    CardNotFound,
    CardSpec,
    TrainingDatabase,
    TrainingNotFound,
    TrainingSpec,
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


async def test_create_card_entry(training_database):
    timestamp = 1
    slots = 10
    card_cost = 200
    card = await training_database.create_card_entry(
        card_spec=CardSpec(
            timestamp=timestamp,
            slots=slots,
            cost=card_cost,
        )
    )

    assert card.timestamp == timestamp
    assert card.slots == slots
    print(type(card.cost))
    assert card.cost == card_cost


async def test_get_card_entry_by_id(training_database):
    timestamp = 1
    slots = 10
    card_cost = 200
    card = await training_database.create_card_entry(
        card_spec=CardSpec(
            timestamp=timestamp,
            slots=slots,
            cost=card_cost,
        )
    )

    actual_card: Card = await training_database.get_card_entry_by_id(card_id=card.id)

    assert actual_card.timestamp == timestamp
    assert actual_card.cost == card_cost
    assert actual_card.slots == slots


async def test_get_card_entry_by_id_fails_if_not_existing(training_database):
    card_id = "some-id"
    with pytest.raises(
        CardNotFound,
        match=f"The requested card entry with id: {card_id} does not exist",
    ):
        await training_database.get_card_entry_by_id(card_id=card_id)


async def test_get_all_card_entries(training_database):
    card_specs = [
        CardSpec(
            timestamp=i + 1,
            cost=200 + 1,
            slots=i + 1,
        )
        for i in range(4)
    ]
    for card_spec in card_specs:
        await training_database.create_card_entry(card_spec=card_spec)

    cards = await training_database.get_all_card_entries()

    assert len(cards) == 4


async def test_get_all_cards_but_not_cards_exists(training_database):
    cards = await training_database.get_all_card_entries()
    assert not cards
