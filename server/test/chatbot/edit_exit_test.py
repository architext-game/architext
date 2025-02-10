from typing import Callable
from architext.chatbot.adapters.fake_messaging_channel import FakeMessagingChannel
from architext.chatbot.adapters.stdout_logger import StdOutLogger
from architext.chatbot.session import Session
import pytest # type: ignore
from test.fixtures import createTestArchitext


@pytest.fixture
def session_factory() -> Callable[[str], Session]:
    def factory(user_id: str):
        architext = createTestArchitext()
        return Session(architext=architext, messaging_channel=FakeMessagingChannel(), logger=StdOutLogger(), user_id=user_id) 
    return factory


def test_edit_exit_name_success(session_factory: Callable[[str], Session]):
    session = session_factory("oliver")

    session.process_message("edit To the spaceship")
    session.process_message("1")
    session.process_message("Hatch")
    session.process_message("asdasd")

    assert isinstance(session.sender.channel, FakeMessagingChannel)
    sender: FakeMessagingChannel = session.sender.channel
    sent_text = '\n'.join([message.text for message in sender._sent])
    print(sent_text)

    assert "Edition completed" in sent_text
    assert "I don't understand that." in sent_text
    uow = session.architext._uow
    olivers = uow.rooms.get_room_by_id("olivers")
    assert olivers is not None
    assert olivers.exits.get("Hatch") is not None
    assert olivers.exits.get("To the spaceship") is None
    

def test_edit_exit_description_success(session_factory: Callable[[str], Session]):
    session = session_factory("oliver")

    session.process_message("edit To the spaceship")
    session.process_message("2")
    session.process_message("This is a great exit! :D")
    session.process_message("asdasd")
    
    assert isinstance(session.sender.channel, FakeMessagingChannel)
    sender: FakeMessagingChannel = session.sender.channel
    sent_text = '\n'.join([message.text for message in sender._sent])
    print(sent_text)

    assert "Edition completed" in sent_text
    assert "I don't understand that." in sent_text
    uow = session.architext._uow
    olivers = uow.rooms.get_room_by_id("olivers")
    assert olivers is not None
    exit = olivers.exits.get("To the spaceship")
    assert exit is not None
    assert exit.description == "This is a great exit! :D"


def test_edit_exit_visibility_success(session_factory: Callable[[str], Session]):
    session = session_factory("oliver")

    session.process_message("edit To the spaceship")
    session.process_message("3")
    session.process_message("Hidden")
    session.process_message("asdasd")
    
    assert isinstance(session.sender.channel, FakeMessagingChannel)
    sender: FakeMessagingChannel = session.sender.channel
    sent_text = '\n'.join([message.text for message in sender._sent])
    print(sent_text)

    assert "Edition completed" in sent_text
    assert "I don't understand that." in sent_text
    uow = session.architext._uow
    olivers = uow.rooms.get_room_by_id("olivers")
    assert olivers is not None
    exit = olivers.exits.get("To the spaceship")
    assert exit is not None
    assert exit.visibility == "hidden"


def test_edit_exit_destination_success(session_factory: Callable[[str], Session]):
    session = session_factory("oliver")

    session.process_message("edit To the spaceship")
    session.process_message("4")
    session.process_message("alices")
    session.process_message("asdasd")
    
    assert isinstance(session.sender.channel, FakeMessagingChannel)
    sender: FakeMessagingChannel = session.sender.channel
    sent_text = '\n'.join([message.text for message in sender._sent])
    print(sent_text)

    assert "Edition completed" in sent_text
    assert "I don't understand that." in sent_text
    uow = session.architext._uow
    olivers = uow.rooms.get_room_by_id("olivers")
    assert olivers is not None
    exit = olivers.exits.get("To the spaceship")
    assert exit is not None
    assert exit.destination_room_id == "alices"