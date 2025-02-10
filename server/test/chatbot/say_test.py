from typing import Callable, cast
from architext.chatbot.adapters.fake_messaging_channel import FakeMessagingChannel
from architext.chatbot.adapters.stdout_logger import StdOutLogger
from architext.chatbot.session import Session
from architext.core.adapters.fake_uow import FakeUnitOfWork
from architext.core.domain.entities.world import DEFAULT_WORLD
from architext.core import Architext
import pytest # type: ignore
from architext.core.domain.entities.user import User
from architext.core.domain.entities.room import Room
from architext.core.domain.entities.exit import Exit
from test.fixtures import createTestArchitext


@pytest.fixture
def session_factory() -> Callable[[str], Session]:
    def factory(user_id: str):
        architext = createTestArchitext()
        return Session(architext=architext, messaging_channel=FakeMessagingChannel(), logger=StdOutLogger(), user_id=user_id) 
    return factory


def test_say_success(session_factory: Callable[[str], Session]):
    return
    bob = session_factory("bob")
    bob_sender = cast(FakeMessagingChannel, bob.sender)

    bob.process_message("say hello dave :-)")

    assert 'bob says "hello dave :-)"' in bob_sender.all_to('dave')