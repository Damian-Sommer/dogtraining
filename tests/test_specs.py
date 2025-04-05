import re

import pytest

from server.training_database import (
    CardSpec,
    CardSpecInvalid,
    TrainingSpec,
    TrainingSpecInvalid,
    TrainingType,
)


async def test_create_training_entry_fails_because_of_invalid_type(
    training_timestamp,
    training_dogs,
    user_id,
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
            dogs=training_dogs,
            card_id="some_string",
            user_id=user_id,
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
    training_type,
    training_dogs,
    training_timestamp,
    user_id,
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
            dogs=training_dogs,
            card_id="some_string",
            user_id=user_id,
        )


@pytest.mark.parametrize(
    "dogs",
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
async def test_create_training_entry_fails_because_of_invalid_dogs(
    training_type,
    training_timestamp,
    dogs,
    user_id,
):
    with pytest.raises(
        TrainingSpecInvalid,
        match=re.escape(
            f"The dogs of a training have to be of type: List[str], but was: {type(dogs)}"
        ),
    ):
        TrainingSpec(
            timestamp=training_timestamp,
            type=training_type,
            dogs=dogs,
            card_id="some_string",
            user_id=user_id,
        )


@pytest.mark.parametrize("card_id", [list(), dict(), set(), None, -1, 1e2, 0])
def test_create_training_spec_fails_because_of_invalid_card_id(
    card_id,
    training_type,
    training_dogs,
    user_id,
):
    with pytest.raises(
        TrainingSpecInvalid,
        match=re.escape(
            f"The card_id of a training has to be of type"
            f" str but was: {card_id} and of type: {type(card_id)}",
        ),
    ):
        TrainingSpec(
            timestamp=1,
            type=training_type,
            dogs=training_dogs,
            card_id=card_id,
            user_id=user_id,
        )


@pytest.mark.parametrize("new_card_id", [list(), dict(), set(), -1, 1e2, 0])
def test_create_training_spec_fails_because_of_invalid_new_card_id(
    new_card_id,
    training_type,
    training_dogs,
    user_id,
):
    with pytest.raises(
        TrainingSpecInvalid,
        match=re.escape(
            f"The new_card_id of a training has to be of type"
            f" str or None but was: {new_card_id} and of type: {type(new_card_id)}",
        ),
    ):
        TrainingSpec(
            timestamp=1,
            type=training_type,
            dogs=training_dogs,
            card_id="some-string",
            new_card_id=new_card_id,
            user_id=user_id,
        )


@pytest.mark.parametrize("user_id", [list(), dict(), set(), -1, 1e2, 0])
def test_create_training_spec_fails_because_of_invalid_user_id(
    user_id, training_type, training_dogs
):
    with pytest.raises(
        TrainingSpecInvalid,
        match=re.escape(
            f"The user_id of a training has to be of type"
            f" str but was: {user_id} and of type: {type(user_id)}",
        ),
    ):
        TrainingSpec(
            timestamp=1,
            type=training_type,
            dogs=training_dogs,
            card_id="some-string",
            new_card_id="new_card_id",
            user_id=user_id,
        )


@pytest.mark.parametrize(
    "card_timestamp",
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
async def test_create_card_spec_fails_because_of_invalid_date_timestamp(
    card_timestamp, user_id
):
    with pytest.raises(
        CardSpecInvalid,
        match=re.escape(
            f"The timestamp of a card can not be below 0 and"
            f" has to be of the type int but was: {card_timestamp}"
            f" and of type: {type(card_timestamp)}",
        ),
    ):
        CardSpec(
            timestamp=card_timestamp,
            slots=10,
            cost=200,
            user_id=user_id,
        )


@pytest.mark.parametrize(
    "card_cost",
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
async def test_create_card_spec_fails_because_of_invalid_card_cost(
    card_cost,
    user_id,
):
    with pytest.raises(
        CardSpecInvalid,
        match=re.escape(
            f"The cost of a card can not be below 0 and"
            f" has to be of the type int but was: {card_cost}"
            f" and of type: {type(card_cost)}",
        ),
    ):
        CardSpec(
            timestamp=1,
            slots=10,
            cost=card_cost,
            user_id=user_id,
        )


@pytest.mark.parametrize(
    "card_slots",
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
async def test_create_card_spec_fails_because_of_invalid_card_slots(
    card_slots,
    user_id,
):
    with pytest.raises(
        CardSpecInvalid,
        match=re.escape(
            f"The slots of a card can not be below 0 and"
            f" has to be of the type int but was: {card_slots}"
            f" and of type: {type(card_slots)}",
        ),
    ):
        CardSpec(
            timestamp=1,
            slots=card_slots,
            cost=1,
            user_id=user_id,
        )


@pytest.mark.parametrize("user_id", [list(), dict(), set(), -1, 1e2, 0])
def test_create_card_spec_fails_because_of_invalid_user_id(
    user_id,
):
    with pytest.raises(
        CardSpecInvalid,
        match=re.escape(
            f"The user_id of a card has to be of type"
            f" str but was: {user_id} and of type: {type(user_id)}",
        ),
    ):
        CardSpec(
            timestamp=1,
            slots=10,
            cost=1,
            user_id=user_id,
        )
