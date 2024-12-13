from architext.core.messagebus import MessageBus
from architext.adapters.fake_notificator import FakeNotificator
from architext.adapters.memory_uow import MemoryUnitOfWork
from architext.ports.unit_of_work import UnitOfWork
import pytest
from architext.core.commands import CreateInitialData
from architext.core.domain.entities.room import DEFAULT_ROOM


@pytest.fixture
def empty_uow() -> MemoryUnitOfWork:
    return MemoryUnitOfWork()

@pytest.fixture
def uow() -> MemoryUnitOfWork:
    uow = MemoryUnitOfWork()
    MessageBus().handle(uow, CreateInitialData())
    return uow

@pytest.fixture
def message_bus() -> MessageBus:
    return MessageBus() 

def test_create_initial_data(empty_uow: MemoryUnitOfWork, message_bus: MessageBus):
    message_bus.handle(empty_uow, CreateInitialData())
    assert empty_uow.committed
    assert empty_uow.rooms.get_room_by_id(DEFAULT_ROOM.id) == DEFAULT_ROOM
