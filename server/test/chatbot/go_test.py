from typing import Callable
from architext.chatbot.adapters.fake_sender import FakeSender
from architext.chatbot.adapters.stdout_logger import StdOutLogger
from architext.chatbot.session import Session
from architext.core.adapters.fake_uow import FakeUnitOfWork
from architext.core.domain.entities.world import DEFAULT_WORLD
from architext.core import Architext
import pytest # type: ignore
from architext.core.domain.entities.user import User
from architext.core.domain.entities.room import Room
from architext.core.domain.entities.exit import Exit
from test.fixtures import createTestData


@pytest.fixture
def session_factory() -> Callable[[str], Session]:
    def factory(user_id: str):
        architext = createTestData()
        return Session(architext=architext, sender=FakeSender(architext), logger=StdOutLogger(), user_id=user_id) 
    return factory


def test_go(session_factory: Callable[[str], Session]):
    session = session_factory("oliver")
    session.process_message("go alice")
    assert isinstance(session.sender, FakeSender)
    sender: FakeSender = session.sender

    sent_text = '\n'.join([message.text for message in sender._sent])
    print(sent_text)
    assert sent_text == """Alice's Room
This is Alice's Room

👤 Players here: Oliver, Alice.
⮕ Exits: To the spaceship, To Oliver's Room, To Bob's Room.
"""
