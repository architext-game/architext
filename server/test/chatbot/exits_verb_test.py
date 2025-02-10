from typing import cast
from architext.chatbot.adapters.fake_messaging_channel import FakeMessagingChannel
from architext.chatbot.adapters.stdout_logger import StdOutLogger
from architext.chatbot.session import Session
from architext.core.adapters.fake_uow import FakeUnitOfWork
from architext.core.domain.entities.world import DEFAULT_WORLD
from architext.core import Architext
import pytest # type: ignore
from architext.core.domain.entities.user import User
from architext.core.domain.entities.room import Room
from test.fixtures import createTestArchitext


@pytest.fixture
def session() -> Session:
    architext = createTestArchitext()
    return Session(architext=architext, messaging_channel=FakeMessagingChannel(), logger=StdOutLogger(), user_id="oliver") 

def test_exits_verb(session: Session):
    session.process_message("exits")
    assert isinstance(session.sender.channel, FakeMessagingChannel)
    sender: FakeMessagingChannel = session.sender.channel

    sent_text = '\n'.join([message.text for message in sender._sent])
    print(sent_text)
    assert "To the spaceship" in sent_text
    assert "To Alice's Room" in sent_text
    assert "To Bob's Room" in sent_text
    assert "Visible door to bathroom" in sent_text
    assert "Auto door to bathroom" in sent_text  # auto shows even when it is mentioned
    assert "Secret exit" not in sent_text
    assert "I don't understand that." not in sent_text

    # Check if verb yields control
    session.process_message("adadasdas")
    sent_text = '\n'.join([message.text for message in sender._sent])
    assert "I don't understand that." in sent_text
