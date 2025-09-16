from architext.core.adapters.fake.notifier import FakeNotifier
from architext.core.adapters.fake.uow import FakeUnitOfWork
from architext.core.application.messagebus import MessageBus
from architext.core.application.commands import Command
from unittest.mock import Mock
import pytest # type: ignore


def test_command_handler_is_called() -> None:
    class SomeCommand(Command[str]):
        pass

    fakeHandler = Mock()
    bus = MessageBus(command_handlers={SomeCommand: fakeHandler})
    bus.handle(FakeUnitOfWork(notifier=FakeNotifier()), SomeCommand())

    assert fakeHandler.called


def test_command_without_handlers_raises_exception() -> None:
    class SomeCommand(Command[str]):
        pass
    
    bus = MessageBus({})

    with pytest.raises(KeyError):
        bus.handle(FakeUnitOfWork(notifier=FakeNotifier()), SomeCommand())


@pytest.mark.skip(reason="to do")
def test_event_without_handlers_gracefully_does_nothing():
    pass

