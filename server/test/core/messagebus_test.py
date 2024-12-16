from architext.adapters.memory_uow import MemoryUnitOfWork
from architext.core.messagebus import MessageBus
from architext.core.domain.events import Event
from unittest.mock import Mock


def test_handler_is_called() -> None:
    class SomeEvent(Event):
        pass

    fakeHandler = Mock()
    bus = MessageBus({SomeEvent: [fakeHandler]})
    bus.handle(MemoryUnitOfWork(), SomeEvent())

    assert fakeHandler.called


def test_event_without_handlers_gracefully_does_nothing():
    class SomeEvent(Event):
        pass
    
    bus = MessageBus({})
    bus.handle(MemoryUnitOfWork(), SomeEvent())

