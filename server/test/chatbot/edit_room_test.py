from csv import Error
from typing import Callable
from architext.chatbot import strings
from architext.chatbot.adapters.fake_messaging_channel import FakeMessagingChannel
from architext.chatbot.adapters.stdout_logger import StdOutLogger
from architext.chatbot.session import Session
from architext.core.settings import ROOM_DESCRIPTION_MAX_LENGTH, ROOM_NAME_MAX_LENGTH
import pytest # type: ignore


def test_edit_room_name_success(channel: FakeMessagingChannel, session_factory: Callable[[str], Session]):
    try:
        session = session_factory("oliver")
        
        session.process_message("remodel")
        assert "Editing room Oliver's Room" in channel.unread
        session.process_message("1")
        assert "Enter the new name:" in channel.unread
        session.process_message("MY COOL ROOM!")
        assert "Edition completed" in channel.unread
        session.process_message("asdasd")
        assert "I don't understand that." in channel.unread

        uow = session.architext._uow
        olivers = uow.rooms.get_room_by_id("olivers")
        assert olivers is not None
        assert olivers.name == "MY COOL ROOM!"
    except:
        print(channel.all)
        raise
    

def test_edit_room_description_success(channel: FakeMessagingChannel, session_factory: Callable[[str], Session]):
    try:
        session = session_factory("oliver")
        
        session.process_message("remodel")
        assert "Editing room" in channel.unread
        session.process_message("2")
        assert "description" in channel.unread
        session.process_message("There is a poster that reads \"2112\"")
        assert "Edition completed" in channel.unread
        session.process_message("asdasd")
        assert "I don't understand that." in channel.unread

        uow = session.architext._uow
        olivers = uow.rooms.get_room_by_id("olivers")
        assert olivers is not None
        assert olivers.description == "There is a poster that reads \"2112\""
    except:
        print(channel.all)
        raise


def test_edit_room_by_unprivileged_user_fails(channel: FakeMessagingChannel, session_factory: Callable[[str], Session]):
    try:
        session = session_factory("alice")
        
        session.process_message("remodel")
        assert "You don't have enough privileges to do that here" in channel.unread
    except:
        print(channel.all)
        raise


def test_edit_room_error_messages(channel: FakeMessagingChannel, session_factory: Callable[[str], Session]):
    session = session_factory("oliver")

    session.process_message("remodel")
    # Choose what to edit
    assert 'Editing room' in channel.unread
    session.process_message("")
    assert 'Please enter a number.' in channel.unread
    session.process_message("adas")
    assert 'Please enter a number.' in channel.unread
    session.process_message("3")
    assert 'Please enter the value of one of the options.' in channel.unread

    # Room name
    session.process_message("1")
    assert 'Enter the new name' in channel.unread
    session.process_message("A"*(ROOM_NAME_MAX_LENGTH+1))
    assert "Can't be longer than" in channel.unread
    session.process_message("")
    assert strings.is_empty in channel.unread

    # Room description
    session.process_message("/")
    session.process_message("edit toroid")
    session.process_message("2")
    assert 'Enter the new description' in channel.unread
    session.process_message("")
    session.process_message("A"*(ROOM_DESCRIPTION_MAX_LENGTH+1))
    assert "Can't be longer than" in channel.unread
