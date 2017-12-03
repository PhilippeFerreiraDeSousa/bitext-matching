import pytest
from mixer.backend.django import mixer

# We need to do this so that writing to the DB is possible in our tests.
pytestmark = pytest.mark.django_db


def test_message():
    obj = mixer.blend('core.Message')
    assert obj.pk > 0
