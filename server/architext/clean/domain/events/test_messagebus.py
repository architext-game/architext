from architext.clean.domain.events.messagebus import MessageBus
from architext.clean.domain.events.events import Event
from unittest.mock import Mock


def test_handler_is_called():
    class SomeEvent(Event):
        pass

    fakeHandler = Mock()
    bus = MessageBus({SomeEvent: [fakeHandler]})
    bus.handle(SomeEvent())

    assert fakeHandler.called


def test_event_without_handlers_gracefully_does_nothing():
    class SomeEvent(Event):
        pass
    
    bus = MessageBus({})
    bus.handle(SomeEvent())

