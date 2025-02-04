from typing import cast
import pytest # type: ignore
from architext.core.adapters.fake_uow import FakeUnitOfWork
from architext.core.services.create_initial_data import create_initial_data
from architext.core.commands import CreateInitialData
from architext.core.domain.entities.room import DEFAULT_ROOM
from architext.core import Architext


@pytest.fixture
def architext() -> Architext:
    return Architext(FakeUnitOfWork())


def test_setup_creates_default_room(architext: Architext):
    architext.handle(CreateInitialData())
    assert cast(FakeUnitOfWork, architext._uow).committed
    assert architext._uow.rooms.get_room_by_id(DEFAULT_ROOM.id) == DEFAULT_ROOM


def test_setup_does_not_recreate_the_default_room_if_exists(architext: Architext):
    architext.handle(CreateInitialData())
    default_room = DEFAULT_ROOM.with_changes(description="Modified description")
    with architext._uow:
        architext._uow.rooms.save_room(default_room)
        architext._uow.commit()

    architext.handle(CreateInitialData())

    room = architext._uow.rooms.get_room_by_id(DEFAULT_ROOM.id)
    assert room is not None
    assert room.description == "Modified description"