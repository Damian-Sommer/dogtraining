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
    training_type, training_used_slots, training_timestamp
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
async def test_create_card_spec_fails_because_of_invalid_date_timestamp(card_timestamp):
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
async def test_create_card_spec_fails_because_of_invalid_card_cost(card_cost):
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
async def test_create_card_spec_fails_because_of_invalid_card_slots(card_slots):
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
        )
