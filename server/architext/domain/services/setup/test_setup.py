import pytest
from architext.domain.unit_of_work.fake.fake_uow import FakeUnitOfWork
from architext.domain.services.setup.setup import setup, DEFAULT_ROOM
from architext.domain.entities.room import Room
import json
import copy

@pytest.fixture
def uow() -> FakeUnitOfWork:
    return FakeUnitOfWork()


def test_setup_creates_default_room(uow: FakeUnitOfWork):
    with uow:
        setup(uow)
        uow.commit()
    print("**"+str(uow.rooms.list_rooms()))
    assert uow.committed
    assert uow.rooms.get_room_by_id(DEFAULT_ROOM.id) == DEFAULT_ROOM


def test_setup_does_not_recreate_the_default_room_if_exists(uow: FakeUnitOfWork):
    with uow:
        default_room = copy.deepcopy(DEFAULT_ROOM)
        default_room.description = "Modified description"
        uow.rooms.save_room(default_room)
        uow.commit()

    with uow:
        setup(uow)
        uow.commit()

    room = uow.rooms.get_room_by_id(DEFAULT_ROOM.id)
    assert room is not None
    assert room.description == "Modified description"