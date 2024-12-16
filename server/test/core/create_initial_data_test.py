from architext.core.messagebus import MessageBus
import pytest # type: ignore
from architext.adapters.memory_uow import MemoryUnitOfWork
from architext.core.services.create_initial_data import create_initial_data
from architext.core.commands import CreateInitialData
from architext.core.domain.entities.room import DEFAULT_ROOM, Room
import copy

@pytest.fixture
def uow() -> MemoryUnitOfWork:
    return MemoryUnitOfWork()

@pytest.fixture
def message_bus() -> MessageBus:
    return MessageBus() 

def test_setup_creates_default_room(uow: MemoryUnitOfWork, message_bus: MessageBus):
    with uow:
        message_bus.handle(uow, CreateInitialData())
        uow.commit()
    print("**"+str(uow.rooms.list_rooms()))
    assert uow.committed
    assert uow.rooms.get_room_by_id(DEFAULT_ROOM.id) == DEFAULT_ROOM


def test_setup_does_not_recreate_the_default_room_if_exists(uow: MemoryUnitOfWork, message_bus: MessageBus):
    with uow:
        default_room = copy.deepcopy(DEFAULT_ROOM)
        default_room.description = "Modified description"
        uow.rooms.save_room(default_room)
        uow.commit()

    with uow:
        message_bus.handle(uow, CreateInitialData())
        uow.commit()

    room = uow.rooms.get_room_by_id(DEFAULT_ROOM.id)
    assert room is not None
    assert room.description == "Modified description"