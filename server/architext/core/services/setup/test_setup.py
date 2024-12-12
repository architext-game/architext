from architext.adapters.memory_uow import MemoryUnitOfWork
from architext.core.services.setup import setup
import pytest
from architext.core.domain.entities.room import DEFAULT_ROOM, Room
import copy

@pytest.fixture
def uow() -> MemoryUnitOfWork:
    return MemoryUnitOfWork()


def test_setup_creates_default_room(uow: MemoryUnitOfWork):
    with uow:
        setup(uow)
        uow.commit()
    print("**"+str(uow.rooms.list_rooms()))
    assert uow.committed
    assert uow.rooms.get_room_by_id(DEFAULT_ROOM.id) == DEFAULT_ROOM


def test_setup_does_not_recreate_the_default_room_if_exists(uow: MemoryUnitOfWork):
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