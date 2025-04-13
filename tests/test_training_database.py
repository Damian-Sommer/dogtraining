import re

import pytest

from dogtraining.server.models import Card, Training
from dogtraining.server.training_database import (
    CardFull,
    CardNotFound,
    CardSpec,
    DogNotFound,
    DogSpec,
    DogSpecInvalid,
    TrainingNotFound,
    TrainingSpec,
    TrainingType,
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
    training_type,
    training_timestamp,
    user_id,
    create_card_entry,
    create_training_entry,
    create_dog_entry,
):
    dog = await create_dog_entry()
    dog2 = await create_dog_entry()
    card = await create_card_entry()
    actual_training = await create_training_entry(card_id=card.id, dogs=[dog.id])

    assert actual_training[0].timestamp == training_timestamp
    assert actual_training[0].type == training_type
    assert actual_training[0].dog_id == dog.id
    assert actual_training[0].card_id == card.id
    assert actual_training[0].user_id == user_id


async def test_get_training_entry_by_id(
    training_database,
    training_timestamp,
    training_type,
    training_dogs,
    create_card_entry,
    create_training_entry,
    create_dog_entry,
    user_id,
):
    card = await create_card_entry()
    dog = await create_dog_entry()
    training = await create_training_entry(card_id=card.id, dogs=[dog.id])

    actual_training: Training = await training_database.get_training_entry_by_id(
        training_id=training[0].id, user_id=user_id
    )
    assert actual_training.timestamp == training_timestamp
    assert actual_training.type == training_type
    assert actual_training.dog_id == dog.id
    assert actual_training.card_id == card.id
    assert actual_training.user_id == user_id


async def test_get_training_entry_by_id_fails_because_false_user_id(
    training_database,
    create_card_entry,
    create_training_entry,
    create_dog_entry,
):
    false_user_id = "test2"
    dog = await create_dog_entry()
    card = await create_card_entry()
    training = await create_training_entry(card_id=card.id, dogs=[dog.id])

    with pytest.raises(
        TrainingNotFound,
        match=f"The requested training entry with id: {training[0].id} does not exist",
    ):
        await training_database.get_training_entry_by_id(
            training_id=training[0].id, user_id=false_user_id
        )


async def test_get_training_entry_by_id_fails_if_not_existing(
    training_database,
    user_id,
):
    training_id = "some-id"
    with pytest.raises(
        TrainingNotFound,
        match=f"The requested training entry with id: {training_id} does not exist",
    ):
        await training_database.get_training_entry_by_id(
            training_id=training_id,
            user_id=user_id,
        )


async def test_get_all_training_entries(
    training_database,
    training_type,
    user_id,
):
    card = await training_database.create_card_entry(
        card_spec=CardSpec(
            timestamp=1,
            slots=6,
            cost=2,
            user_id=user_id,
        )
    )

    training_specs = [
        TrainingSpec(
            timestamp=i + 1,
            type=training_type,
            dogs=[str(i + 1)],
            card_id=card.id,
            user_id=user_id,
        )
        for i in range(4)
    ]
    for training_spec in training_specs:
        await training_database.create_training_entry(training_spec=training_spec)

    trainings = await training_database.get_all_training_entries(user_id=user_id)

    assert len(trainings) == 4


async def test_get_all_trainings_but_not_training_exists(training_database, user_id):
    trainings = await training_database.get_all_training_entries(
        user_id=user_id,
    )
    assert not trainings


async def test_create_card_entry(training_database, user_id):
    timestamp = 1
    slots = 10
    card_cost = 200
    card = await training_database.create_card_entry(
        card_spec=CardSpec(
            timestamp=timestamp,
            slots=slots,
            cost=card_cost,
            user_id=user_id,
        )
    )

    assert card.timestamp == timestamp
    assert card.slots == slots
    assert card.cost == card_cost
    assert card.user_id == user_id


async def test_get_card_entry_by_id(
    training_database,
    create_card_entry,
    user_id,
):
    card: Card = await create_card_entry()

    actual_card: Card = await training_database.get_card_entry_by_id(
        card_id=card.id,
        user_id=user_id,
    )

    assert actual_card.timestamp == card.timestamp
    assert actual_card.cost == card.cost
    assert actual_card.slots == card.slots
    assert actual_card.user_id == card.user_id


async def test_get_card_entry_by_id_fails_if_not_existing(
    training_database,
    user_id,
):
    card_id = "some-id"
    with pytest.raises(
        CardNotFound,
        match=f"The requested card entry with id: {card_id} does not exist",
    ):
        await training_database.get_card_entry_by_id(
            card_id=card_id,
            user_id=user_id,
        )


async def test_get_card_entry_by_id_fails_because_false_user_id(
    create_card_entry,
    training_database,
):
    false_user_id = "some-id"
    card = await create_card_entry()
    with pytest.raises(
        CardNotFound,
        match=f"The requested card entry with id: {card.id} does not exist",
    ):
        await training_database.get_card_entry_by_id(
            card_id=card.id,
            user_id=false_user_id,
        )


async def test_get_trainings_by_referenced_card_id(
    training_database,
    create_training_entry,
    create_card_entry,
    create_dog_entry,
    user_id,
):
    card: Card = await create_card_entry()
    dog = await create_dog_entry()
    training: Training = await create_training_entry(card_id=card.id, dogs=[dog.id])

    actual_card = await training_database.get_card_entry_by_id(
        card_id=card.id, user_id=user_id
    )
    assert len(actual_card.trainings) == 1
    assert actual_card.trainings[0].id == training[0].id


async def test_get_card_by_referenced_in_training(
    create_card_entry,
    create_training_entry,
    create_dog_entry,
    training_database,
    user_id,
):
    card = await create_card_entry()
    dog = await create_dog_entry()

    training = await create_training_entry(card_id=card.id, dogs=[dog.id])

    actual_training = await training_database.get_training_entry_by_id(
        training_id=training[0].id, user_id=user_id
    )
    assert actual_training.card.id == card.id


async def test_get_all_card_entries(
    training_database,
    user_id,
):
    card_specs = [
        CardSpec(
            timestamp=i + 1,
            cost=200 + 1,
            slots=i + 1,
            user_id=user_id,
        )
        for i in range(4)
    ]
    for card_spec in card_specs:
        await training_database.create_card_entry(card_spec=card_spec)

    cards = await training_database.get_all_card_entries(user_id=user_id)

    assert len(cards) == 4


async def test_get_all_cards_but_not_cards_exists(training_database, user_id):
    cards = await training_database.get_all_card_entries(user_id=user_id)
    assert not cards


async def test_get_training_entry_as_dict(
    create_training_entry,
    create_dog_entry,
    training_timestamp,
    training_type,
    training_dogs,
    create_card_entry,
    user_id,
):
    card = await create_card_entry()
    dog = await create_dog_entry()
    training = await create_training_entry(card_id=card.id, dogs=[dog.id])
    assert (
        training[0].as_dict().items()
        == dict(
            id=training[0].id,
            timestamp=training_timestamp,
            type=training_type,
            dog_id=dog.id,
            card_id=card.id,
            user_id=user_id,
        ).items()
    )


async def test_get_card_entry_as_dict(
    create_card_entry,
    user_id,
):
    card = await create_card_entry()
    assert (
        card.as_dict().items()
        == dict(
            id=card.id,
            timestamp=card.timestamp,
            cost=card.cost,
            slots=card.slots,
            user_id=user_id,
        ).items()
    )


async def test_create_training_entry_but_card_is_full_raises_exception(
    training_database,
    create_card_entry,
    training_timestamp,
    training_type,
    user_id,
):
    card = await create_card_entry()
    with pytest.raises(
        CardFull,
        match=f"The card: {card.id} has not enough slots for this training entry, please create a new card entry with and provide it as 'new_card' in the payload.",
    ):
        await training_database.create_training_entry(
            training_spec=TrainingSpec(
                timestamp=training_timestamp,
                card_id=card.id,
                type=training_type,
                dogs=["some-0", "some-1"],
                user_id=user_id,
            )
        )


async def test_create_training_entry_but_assign_overflowing_trainings_to_new_card(
    training_database,
    create_card_entry,
    training_timestamp,
    training_type,
    user_id,
):
    card = await create_card_entry()
    card_new = await create_card_entry()
    trainings = await training_database.create_training_entry(
        training_spec=TrainingSpec(
            timestamp=training_timestamp,
            card_id=card.id,
            new_card_id=card_new.id,
            type=training_type,
            dogs=["some-0", "some-1"],
            user_id=user_id,
        )
    )

    assert trainings[0].card_id == card.id
    assert trainings[1].card_id == card_new.id


@pytest.mark.parametrize(
    "registration_time",
    [
        "wfe",
        list(),
        dict(),
        -1,
    ],
)
async def test_dog_spec_registration_time_invalid(
    user_id,
    registration_time,
):
    with pytest.raises(
        DogSpecInvalid,
        match=re.escape(
            f"The registration_time of a dog can not be below 0 and "
            f"has to be of the type int but was: {registration_time} and "
            f"of type: {type(registration_time)}"
        ),
    ):
        DogSpec(
            registration_time=registration_time,
            name="test",
            user_id=user_id,
        )


@pytest.mark.parametrize(
    "name",
    [
        list(),
        dict(),
        -1,
    ],
)
async def test_dog_spec_name_invalid(
    user_id,
    name,
):
    with pytest.raises(
        DogSpecInvalid,
        match=re.escape(
            f"The name of a dog has to be of type str but was: {name} "
            f"and of type: {type(name)}"
        ),
    ):
        DogSpec(
            registration_time=738,
            name=name,
            user_id=user_id,
        )


@pytest.mark.parametrize(
    "user_id",
    [
        list(),
        dict(),
        -1,
    ],
)
async def test_dog_spec_user_id_invalid(
    user_id,
):
    with pytest.raises(
        DogSpecInvalid,
        match=re.escape(
            f"The user_id of a dog has to be of type str but was: {user_id} "
            f"and of type: {type(user_id)}"
        ),
    ):
        DogSpec(
            registration_time=738,
            name="test",
            user_id=user_id,
        )


async def test_create_dog_entry(
    user_id, create_dog_entry, dog_name, dog_registration_time
):
    dog = await create_dog_entry()

    assert dog.name == dog_name
    assert dog.registration_time == dog_registration_time
    assert dog.user_id == user_id


async def test_create_dog_entry_by_id(
    training_database,
    user_id,
    create_dog_entry,
):
    expected_dog = await create_dog_entry()
    actual_dog = await training_database.get_dog_by_id(
        dog_id=expected_dog.id, user_id=user_id
    )

    assert expected_dog.name == actual_dog.name
    assert expected_dog.user_id == actual_dog.user_id


async def test_get_dog_by_id_but_no_dog_exists(
    training_database,
    user_id,
):
    dog_id = "test_dog"
    with pytest.raises(
        DogNotFound, match=f"The requested dog entry with id: {dog_id} does not exist"
    ):
        await training_database.get_dog_by_id(dog_id=dog_id, user_id=user_id)


async def test_get_all_dogs(
    training_database,
    create_dog_entry,
    user_id,
    dog_registration_time,
    dog_name,
):
    dog = await create_dog_entry()

    await training_database.create_dog_entry(
        dog_spec=DogSpec(
            registration_time=dog_registration_time,
            name=dog_name,
            user_id="tjiwoa",
        )
    )

    dogs = await training_database.get_all_dogs(user_id=user_id)

    assert len(dogs) == 1
    assert dogs[0].id == dog.id
