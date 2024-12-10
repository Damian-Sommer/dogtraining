import pytest

from server.training_database import TrainingType


@pytest.fixture
def training_timestamp():
    return 1


@pytest.fixture
def training_used_slots():
    return 1


@pytest.fixture
def training_type():
    return TrainingType.ALLTAGSSPAZIERGANG
