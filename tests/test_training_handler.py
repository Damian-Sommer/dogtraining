import attrs
import pytest
from aiohttp import web

from dogtraining.server.models import Card
from dogtraining.server.training_database import CardSpec, TrainingSpec
from dogtraining.server.training_handler import TrainingHandler


@pytest.fixture
async def client(aiohttp_client, training_database):
    training_handler = TrainingHandler(training_database=training_database)
    app = web.Application()
    app.add_routes(
        [
            web.get("/trainings", training_handler.get_all_trainings),
            web.get("/trainings/{id}", training_handler.get_training_by_id),
            web.get("/cards", training_handler.get_all_cards),
            web.get("/cards/{id}", training_handler.get_card_by_id),
            web.post("/cards", training_handler.create_card_entry),
            web.post("/trainings", training_handler.create_training_entry),
        ]
    )
    return await aiohttp_client(app)


async def test_get_all_trainings(client, create_card_entry, create_training_entry):
    card = await create_card_entry()
    training = await create_training_entry(card_id=card.id)
    response = await client.get("/trainings")
    assert response.status == 200
    trainings = await response.json()
    assert len(trainings) == 1
    assert trainings == [training[0].as_dict()]


async def test_return_exception_if_training_does_not_exist(client):
    training_id = "some-id"
    response: web.Response = await client.get(f"/trainings/{training_id}")
    assert response.status == 400
    training_resp = await response.json()
    assert training_resp == {
        "error": f"The requested training entry with id: {training_id} does not exist"
    }


async def test_get_training_by_id(client, create_card_entry, create_training_entry):
    card = await create_card_entry()
    training = await create_training_entry(card_id=card.id)
    response = await client.get(f"/trainings/{training[0].id}")
    assert response.status == 200
    training_resp = await response.json()
    assert training_resp == training[0].as_dict()


async def test_get_all_card_entries(client, create_card_entry):
    card = await create_card_entry()
    response = await client.get("/cards")
    assert response.status == 200
    cards = await response.json()
    assert cards == [card.as_dict()]


async def test_return_exception_if_card_does_not_exist(client):
    card_id = "some-id"
    response = await client.get(f"/cards/{card_id}")
    assert response.status == 400
    assert await response.json() == {
        "error": f"The requested card entry with id: {card_id} does not exist",
    }


async def test_get_card_by_id(client, create_card_entry):
    card = await create_card_entry()
    response = await client.get(f"/cards/{card.id}")
    assert response.status == 200
    assert await response.json() == card.as_dict()


async def test_create_card_entry_with_valid_data_succeeds(client):
    card_spec = CardSpec(
        timestamp=2,
        slots=2,
        cost=3,
    )
    response = await client.post("/cards", json=attrs.asdict(card_spec))
    assert response.status == 200
    assert (await response.json()).items() >= attrs.asdict(card_spec).items()


async def test_create_card_entry_with_invalid_payload_fails(client):
    response = await client.post("/cards", json=dict(some="value"))
    assert response.status == 400
    assert await response.json() == {
        "error": f"You have to provide a payload with the following keys: {["timestamp", "cost", "slots"]}"
    }


async def test_create_training_entry_with_invalid_payload_fails(client):
    response = await client.post("/trainings", json=dict(some="value"))
    assert response.status == 400
    assert await response.json() == {
        "error": f"You have to provide a payload with the following keys: {["timestamp", "type", "dogs", "card_id"]}"
    }


async def test_create_training_entry_but_card_does_not_exist(
    client, training_timestamp, training_type, training_dogs
):
    card_id = "some-id"
    training_spec = TrainingSpec(
        timestamp=training_timestamp,
        type=training_type,
        dogs=training_dogs,
        card_id=card_id,
    )
    response = await client.post("/trainings", json=attrs.asdict(training_spec))
    assert response.status == 400
    assert await response.json() == {
        "error": f"The requested card entry with id: {card_id} does not exist"
    }


async def test_create_training_entry_with_valid_data_succeeds(
    client,
    create_card_entry,
    training_timestamp,
    training_type,
    training_dogs,
):
    card = await create_card_entry()
    training_spec = TrainingSpec(
        timestamp=training_timestamp,
        type=training_type,
        dogs=training_dogs,
        card_id=card.id,
    )
    response = await client.post("/trainings", json=attrs.asdict(training_spec))
    assert response.status == 200
    assert (await response.json())[0].items() >= dict(
        timestamp=training_timestamp,
        dog=training_dogs[0],
        type=training_type,
    ).items()


async def test_create_training_entry_but_card_will_be_overflown_raises_exception(
    client,
    create_card_entry,
    training_type,
    training_timestamp,
):
    card = await create_card_entry()
    training_spec = TrainingSpec(
        timestamp=training_timestamp,
        type=training_type,
        dogs=["some", "dog"],
        card_id=card.id,
    )
    response = await client.post("/trainings", json=attrs.asdict(training_spec))
    assert response.status == 400
    assert await response.json() == {
        "error": f"The card: {card.id} has not enough slots for this training entry, please create a new card entry with and provide it as 'new_card' in the payload.",
    }


async def test_create_training_entry_but_card_will_be_overflown(
    client,
    create_card_entry,
    training_type,
    training_timestamp,
):
    dogs = ["some", "dog"]
    card: Card = await create_card_entry()
    card_new: Card = await create_card_entry()
    training_spec = TrainingSpec(
        timestamp=training_timestamp,
        type=training_type,
        dogs=dogs,
        card_id=card.id,
        new_card_id=card_new.id,
    )
    response = await client.post("/trainings", json=attrs.asdict(training_spec))
    assert response.status == 200
    response_json = await response.json()
    assert (
        response_json[0].items()
        >= dict(
            timestamp=training_timestamp,
            dog=dogs[0],
            type=training_type,
            card_id=card.id,
        ).items()
    )
    assert (
        response_json[1].items()
        >= dict(
            timestamp=training_timestamp,
            dog=dogs[1],
            type=training_type,
            card_id=card_new.id,
        ).items()
    )
