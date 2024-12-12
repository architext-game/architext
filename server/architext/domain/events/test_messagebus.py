from architext.domain.events.messagebus import MessageBus
from architext.domain.events.events import Event
from unittest.mock import Mock
from architext.domain.unit_of_work.fake.fake_uow import FakeUnitOfWork


def test_handler_is_called() -> None:
    class SomeEvent(Event):
        pass

    fakeHandler = Mock()
    bus = MessageBus({SomeEvent: [fakeHandler]})
    bus.handle(FakeUnitOfWork(), SomeEvent())

    assert fakeHandler.called


def test_event_without_handlers_gracefully_does_nothing():
    class SomeEvent(Event):
        pass
    
    bus = MessageBus({})
    bus.handle(FakeUnitOfWork(), SomeEvent())

