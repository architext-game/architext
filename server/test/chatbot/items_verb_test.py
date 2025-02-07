from typing import cast
from architext.chatbot.adapters.fake_sender import FakeSender
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
    return Session(architext=architext, sender=FakeSender(architext), logger=StdOutLogger(), user_id="oliver") 


def test_items_verb_show_items(session: Session):
    session.process_message("items")
    assert isinstance(session.sender, FakeSender)
    sender: FakeSender = session.sender

    sent_text = '\n'.join([message.text for message in sender._sent])
    print(sent_text)
    assert "A cube" in sent_text  
    assert "A sphere" in sent_text
    assert "A small cube" in sent_text
    assert "A toroid" in sent_text


def test_item_verb_dont_show_hidden_items(session: Session):
    session.process_message("items")
    assert isinstance(session.sender, FakeSender)
    sender: FakeSender = session.sender

    sent_text = '\n'.join([message.text for message in sender._sent])
    print(sent_text)
    assert "A pyramid" not in sent_text


    
