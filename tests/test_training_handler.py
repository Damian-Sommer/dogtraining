import attrs
import pytest
from aiohttp import web

from dogtraining.server.models import Card
from dogtraining.server.training_database import (
    CardSpec,
    DogSpec,
    TrainingSpec,
    TrainingType,
)
from dogtraining.server.training_handler import TrainingHandler, user_authentication


@pytest.fixture
async def client(aiohttp_client, training_database):
    training_handler = TrainingHandler(training_database=training_database)
    app = web.Application(middlewares=[user_authentication])
    app.add_routes(
        [
            web.get("/trainings", training_handler.get_all_trainings),
            web.get("/trainings/{id}", training_handler.get_training_by_id),
            web.get("/cards", training_handler.get_all_cards),
            web.get("/cards/{id}", training_handler.get_card_by_id),
            web.post("/cards", training_handler.create_card_entry),
            web.post("/trainings", training_handler.create_training_entry),
            web.get("/training_types", training_handler.get_all_training_types),
            web.post("/dogs", training_handler.create_dog_entry),
            web.get("/dogs", training_handler.get_all_dogs),
            web.get("/dogs/{id}", training_handler.get_dog_by_id),
        ]
    )
    return await aiohttp_client(app)


async def test_user_id_is_not_in_request_header_returns_error(client):
    response = await client.get("/trainings")
    assert response.status == 401
    assert (await response.json()) == {
        "error": "Unauthorized access, provide the correct authorization header."
    }


async def test_get_all_trainings(
    client,
    create_card_entry,
    create_training_entry,
    create_dog_entry,
    user_id,
):
    await create_card_entry()

    dog = await create_dog_entry()
    training = await create_training_entry(dogs=[dog.id])
    response = await client.get("/trainings", headers={"user_id": user_id})
    assert response.status == 200
    trainings = await response.json()
    assert len(trainings) == 1
    assert trainings == [training[0].as_dict()]


async def test_return_exception_if_training_does_not_exist(client, user_id):
    training_id = "some-id"
    response: web.Response = await client.get(
        f"/trainings/{training_id}", headers={"user_id": user_id}
    )
    assert response.status == 400
    training_resp = await response.json()
    assert training_resp == {
        "error": f"The requested training entry with id: {training_id} does not exist"
    }


async def test_get_training_by_id(
    client,
    create_card_entry,
    create_training_entry,
    create_dog_entry,
    user_id,
):
    await create_card_entry()

    dog = await create_dog_entry()
    training = await create_training_entry(dogs=[dog.id])
    response = await client.get(
        f"/trainings/{training[0].id}", headers={"user_id": user_id}
    )
    assert response.status == 200
    training_resp = await response.json()
    assert training_resp == training[0].as_dict()


async def test_get_all_card_entries(client, create_card_entry, user_id):
    card = await create_card_entry()
    response = await client.get("/cards", headers={"user_id": user_id})
    assert response.status == 200
    cards = await response.json()
    assert cards == [card.as_dict()]


async def test_return_exception_if_card_does_not_exist(client, user_id):
    card_id = "some-id"
    response = await client.get(f"/cards/{card_id}", headers={"user_id": user_id})
    assert response.status == 400
    assert await response.json() == {
        "error": f"The requested card entry with id: {card_id} does not exist",
    }


async def test_get_card_by_id(client, create_card_entry, user_id):
    card = await create_card_entry()
    response = await client.get(f"/cards/{card.id}", headers={"user_id": user_id})
    assert response.status == 200
    assert await response.json() == card.as_dict()


async def test_create_card_entry_with_valid_data_succeeds(client, user_id):
    card_spec = CardSpec(
        timestamp=2,
        slots=2,
        cost=3,
        user_id=user_id,
    )
    response = await client.post(
        "/cards", json=attrs.asdict(card_spec), headers={"user_id": user_id}
    )
    assert response.status == 200
    assert (await response.json()).items() >= attrs.asdict(card_spec).items()


async def test_create_card_entry_with_invalid_payload_fails(client, user_id):
    response = await client.post(
        "/cards", json=dict(some="value"), headers={"user_id": user_id}
    )
    assert response.status == 400
    assert await response.json() == {
        "error": f"You have to provide a payload with the following keys: {["timestamp", "cost", "slots"]}"
    }


async def test_create_training_entry_with_invalid_payload_fails(client, user_id):
    response = await client.post(
        "/trainings", json=dict(some="value"), headers={"user_id": user_id}
    )
    assert response.status == 400
    assert await response.json() == {
        "error": f"You have to provide a payload with the following keys: {["timestamp", "type", "dogs"]}"
    }


async def test_create_training_entry_but_card_does_not_exist(
    client,
    training_timestamp,
    training_type,
    training_dogs,
    user_id,
):
    training_spec = TrainingSpec(
        timestamp=training_timestamp,
        type=training_type,
        dogs=training_dogs,
        user_id=user_id,
    )
    response = await client.post(
        "/trainings", json=attrs.asdict(training_spec), headers={"user_id": user_id}
    )
    assert response.status == 400
    assert await response.json() == {
        "error": "Only 0 slot available but 1 amount of slots are required, register a new card first before trying this operation again."
    }


async def test_create_training_entry_with_valid_data_succeeds(
    client,
    create_card_entry,
    training_timestamp,
    create_dog_entry,
    training_type,
    training_dogs,
    user_id,
):
    dog = await create_dog_entry()
    await create_card_entry()
    training_spec = TrainingSpec(
        timestamp=training_timestamp,
        type=training_type,
        dogs=[dog.id],
        user_id=user_id,
    )
    response = await client.post(
        "/trainings", json=attrs.asdict(training_spec), headers={"user_id": user_id}
    )
    assert response.status == 200
    assert (await response.json())[0].items() >= dict(
        timestamp=training_timestamp,
        dog_id=dog.id,
        type=training_type,
    ).items()


async def test_create_training_entry_but_card_will_be_overflown_raises_exception(
    client,
    create_card_entry,
    training_type,
    training_timestamp,
    user_id,
):
    await create_card_entry()
    training_spec = TrainingSpec(
        timestamp=training_timestamp,
        type=training_type,
        dogs=["some", "dog"],
        user_id=user_id,
    )
    response = await client.post(
        "/trainings", json=attrs.asdict(training_spec), headers={"user_id": user_id}
    )
    assert response.status == 400
    assert await response.json() == {
        "error": "Only 1 slot available but 2 amount of slots are required, register a new card first before trying this operation again.",
    }


async def test_create_two_training_entries_with_two_card_entries(
    client,
    create_card_entry,
    training_type,
    create_dog_entry,
    training_timestamp,
    user_id,
):
    dog = await create_dog_entry()
    dog2 = await create_dog_entry()
    card: Card = await create_card_entry()
    card_new: Card = await create_card_entry()
    training_spec = TrainingSpec(
        timestamp=training_timestamp,
        type=training_type,
        dogs=[dog.id, dog2.id],
        user_id=user_id,
    )
    response = await client.post(
        "/trainings", json=attrs.asdict(training_spec), headers={"user_id": user_id}
    )
    assert response.status == 200
    response_json = await response.json()
    assert (
        response_json[0].items()
        >= dict(
            timestamp=training_timestamp,
            dog_id=dog.id,
            type=training_type,
            card_id=card.id,
            user_id=user_id,
        ).items()
    )
    assert (
        response_json[1].items()
        >= dict(
            timestamp=training_timestamp,
            dog_id=dog2.id,
            type=training_type,
            card_id=card_new.id,
            user_id=user_id,
        ).items()
    )


async def test_get_all_training_types(client, user_id):
    response = await client.get("/training_types", headers={"user_id": user_id})
    assert response.status == 200
    response_json = await response.json()
    assert response_json == [type.value for type in TrainingType]


async def test_register_dogs_in_database_fails_invalid_registration_time(
    client,
    user_id,
):
    response = await client.post(
        "/dogs",
        json={},
        headers={"user_id": user_id},
    )
    assert response.status == 400
    response_json = await response.json()

    assert response_json == {
        "error": f"You have to provide a payload with the following keys: {["registration_time", "name"]}"
    }


async def test_get_dog_by_id(client, create_dog_entry, user_id):
    dog = await create_dog_entry()

    response = await client.get(
        f"/dogs/{dog.id}",
        headers={"user_id": user_id},
    )

    assert response.status == 200
    response_json = await response.json()
    assert (
        response_json.items()
        == dict(
            id=dog.id,
            registration_time=dog.registration_time,
            name=dog.name,
            user_id=user_id,
        ).items()
    )


async def test_get_all_dogs(
    client,
    create_dog_entry,
    training_database,
    user_id,
    dog_name,
    dog_registration_time,
):
    dog = await create_dog_entry()

    await training_database.create_dog_entry(
        dog_spec=DogSpec(
            registration_time=dog_registration_time,
            name=dog_name,
            user_id="tjiwoa",
        )
    )

    response = await client.get(
        "/dogs",
        headers={"user_id": user_id},
    )

    assert response.status == 200
    response_json = await response.json()
    assert len(response_json) == 1
    assert (
        response_json[0].items()
        == dict(
            id=dog.id,
            registration_time=dog.registration_time,
            name=dog.name,
            user_id=user_id,
        ).items()
    )
