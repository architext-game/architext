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

def test_look_room_shows_name_and_description(session: Session):
    session.process_message("look")
    assert isinstance(session.sender.channel, FakeMessagingChannel)
    sender: FakeMessagingChannel = session.sender.channel

    sent_text = '\n'.join([message.text for message in sender._sent])
    print(sent_text)
    assert "Oliver's Room" in sent_text
    assert "This is Oliver's Room" in sent_text


def test_look_room_shows_exits(session: Session):
    session.process_message("look")
    assert isinstance(session.sender.channel, FakeMessagingChannel)
    sender: FakeMessagingChannel = session.sender.channel

    sent_text = '\n'.join([message.text for message in sender._sent])
    print(sent_text)
    assert "To the spaceship" in sent_text
    assert "To Alice's Room" in sent_text
    assert "To Bob's Room" in sent_text


def test_look_room_dont_show_hidden_exits(session: Session):
    session.process_message("look")
    assert isinstance(session.sender.channel, FakeMessagingChannel)
    sender: FakeMessagingChannel = session.sender.channel

    sent_text = '\n'.join([message.text for message in sender._sent])
    print(sent_text)
    assert "Secret exit" not in sent_text

    # It's easy for this test to give a false positive 
    # if the secret exit is removed from the fixtures,
    # so let'd check that it's still there
    uow = cast(FakeUnitOfWork, session.architext._uow)
    with uow as transaction:
        room = transaction.rooms.get_room_by_id("olivers")
        assert room is not None
        exit = room.exits.get("Secret exit")
        assert exit is not None


def test_look_room_dont_show_visible_exits(session: Session):
    session.process_message("look")
    assert isinstance(session.sender.channel, FakeMessagingChannel)
    sender: FakeMessagingChannel = session.sender.channel

    sent_text = '\n'.join([message.text for message in sender._sent])
    print(sent_text)
    assert "Visible door to bathroom" not in sent_text


def test_look_room_dont_show_auto_visibility_exits_mentioned_in_room_description(session: Session):
    session.process_message("look")
    assert isinstance(session.sender.channel, FakeMessagingChannel)
    sender: FakeMessagingChannel = session.sender.channel

    sent_text = '\n'.join([message.text for message in sender._sent])
    print(sent_text)

    after_room_description = sent_text.split("⮕ Exits: ", 1)[1]

    assert "Auto door to bathroom" not in after_room_description


def test_look_room_shows_items(session: Session):
    session.process_message("look")
    assert isinstance(session.sender.channel, FakeMessagingChannel)
    sender: FakeMessagingChannel = session.sender.channel

    sent_text = '\n'.join([message.text for message in sender._sent])
    print(sent_text)

    after_room_description = sent_text.split("👁 You see", 1)[1]

    assert "A cube" in after_room_description  # not mentioned auto
    assert "A sphere" in after_room_description  # listed
    assert "A small cube" not in after_room_description  # mentioned auto
    assert "A toroid" not in after_room_description  # unlisted
    assert "A pyramid" not in after_room_description  # hidden
