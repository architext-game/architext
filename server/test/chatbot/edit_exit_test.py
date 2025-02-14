from typing import Callable
from architext.chatbot import strings
from architext.chatbot.adapters.fake_messaging_channel import FakeMessagingChannel
from architext.chatbot.adapters.stdout_logger import StdOutLogger
from architext.chatbot.session import Session
from architext.core.settings import EXIT_NAME_MAX_LENGTH, EXIT_DESCRIPTION_MAX_LENGTH
import pytest # type: ignore


def test_edit_exit_name_success(channel: FakeMessagingChannel, session_factory: Callable[[str], Session]):
    session = session_factory("oliver")

    session.process_message("edit To the spaceship")
    session.process_message("1")
    session.process_message("Hatch")
    session.process_message("asdasd")

    sent_text = channel.all
    print(sent_text)

    assert "Edition completed" in sent_text
    assert "I don't understand that." in sent_text
    uow = session.architext._uow
    olivers = uow.rooms.get_room_by_id("olivers")
    assert olivers is not None
    assert olivers.exits.get("Hatch") is not None
    assert olivers.exits.get("To the spaceship") is None
    

def test_edit_exit_description_success(channel: FakeMessagingChannel, session_factory: Callable[[str], Session]):
    session = session_factory("oliver")

    session.process_message("edit To the spaceship")
    session.process_message("2")
    session.process_message("This is a great exit! :D")
    session.process_message("asdasd")
    
    sent_text = channel.all
    print(sent_text)

    assert "Edition completed" in sent_text
    assert "I don't understand that." in sent_text
    uow = session.architext._uow
    olivers = uow.rooms.get_room_by_id("olivers")
    assert olivers is not None
    exit = olivers.exits.get("To the spaceship")
    assert exit is not None
    assert exit.description == "This is a great exit! :D"


def test_edit_exit_visibility_success(channel: FakeMessagingChannel, session_factory: Callable[[str], Session]):
    session = session_factory("oliver")

    session.process_message("edit To the spaceship")
    session.process_message("3")
    session.process_message("Hidden")
    session.process_message("asdasd")
    
    sent_text = channel.all
    print(sent_text)

    assert "Edition completed" in sent_text
    assert "I don't understand that." in sent_text
    uow = session.architext._uow
    olivers = uow.rooms.get_room_by_id("olivers")
    assert olivers is not None
    exit = olivers.exits.get("To the spaceship")
    assert exit is not None
    assert exit.visibility == "hidden"


def test_edit_exit_destination_success(channel: FakeMessagingChannel, session_factory: Callable[[str], Session]):
    session = session_factory("oliver")

    session.process_message("edit To the spaceship")
    session.process_message("4")
    session.process_message("alices")
    session.process_message("asdasd")
    
    sent_text = channel.all
    print(sent_text)

    assert "Edition completed" in sent_text
    assert "I don't understand that." in sent_text
    uow = session.architext._uow
    olivers = uow.rooms.get_room_by_id("olivers")
    assert olivers is not None
    exit = olivers.exits.get("To the spaceship")
    assert exit is not None
    assert exit.destination_room_id == "alices"


def test_edit_by_unauthorized_user_fails(channel: FakeMessagingChannel, session_factory: Callable[[str], Session]):
    session = session_factory("alice")

    session.process_message("edit To the spaceship")
    assert "You don't have enough privileges to do that here" in channel.unread


def test_edit_exit_error_messages(channel: FakeMessagingChannel, session_factory: Callable[[str], Session]):
    session = session_factory("oliver")

    session.process_message("edit To the spaceship")
    # Choose what to edit
    assert 'Editing exit' in channel.unread
    session.process_message("")
    assert 'Please enter a number.' in channel.unread
    session.process_message("adas")
    assert 'Please enter a number.' in channel.unread
    session.process_message("9")
    assert 'Please enter the value of one of the options.' in channel.unread

    # Exit name
    session.process_message("1")
    assert 'Enter the new name' in channel.unread
    session.process_message("A"*(EXIT_NAME_MAX_LENGTH+1))
    assert "Can't be longer than" in channel.unread
    session.process_message("")
    assert strings.is_empty in channel.unread

    # Exit description
    session.process_message("/")
    session.process_message("edit To the spaceship")
    session.process_message("2")
    assert 'Enter the new description' in channel.unread
    session.process_message("")
    session.process_message("A"*(EXIT_DESCRIPTION_MAX_LENGTH+1))
    assert "Can't be longer than" in channel.unread

    # Exit visibility
    session.process_message("/")
    session.process_message("edit To the spaceship")
    session.process_message("3")
    assert 'Choose the new visibility' in channel.unread
    session.process_message("")
    assert "It can't be empty, try with another one" in channel.unread
    session.process_message("asdas")
    assert "Please enter the value of one of the options." in channel.unread

    # Exit destination
    session.process_message("/")
    session.process_message("edit To the spaceship")
    session.process_message("4")
    assert 'Enter the room number of the new destination' in channel.unread
    session.process_message("")
    assert "It can't be empty, try with another one" in channel.unread
    session.process_message("asdas")
    assert strings.room_not_found in channel.unread
