from typing import Callable
from architext.chatbot import strings
from architext.chatbot.adapters.fake_messaging_channel import FakeMessagingChannel
from architext.chatbot.adapters.stdout_logger import StdOutLogger
from architext.chatbot.session import Session
from architext.core.settings import ITEM_DESCRIPTION_MAX_LENGTH, ITEM_NAME_MAX_LENGTH
import pytest # type: ignore


def test_edit_item_name_success(session_factory: Callable[[str], Session]):
    session = session_factory("oliver")

    session.process_message("edit toroid")
    session.process_message("1")
    session.process_message("A Donut")
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
    assert olivers.items.get("A Donut") is not None
    assert olivers.items.get("A Toroid") is None
    

def test_edit_item_description_success(session_factory: Callable[[str], Session]):
    session = session_factory("oliver")

    session.process_message("edit Toroid")
    session.process_message("2")
    session.process_message("It's just like a donut")
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
    item = olivers.items.get("A toroid")
    assert item is not None
    assert item.description == "It's just like a donut"


def test_edit_item_visibility_success(session_factory: Callable[[str], Session]):
    session = session_factory("oliver")

    session.process_message("edit A Toroid")
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
    item = olivers.items.get("A toroid")
    assert item is not None
    assert item.visibility == "hidden"


def test_edit_item_error_messages(channel: FakeMessagingChannel, session_factory: Callable[[str], Session]):
    session = session_factory("oliver")

    session.process_message("edit toroid")
    # Choose what to edit
    assert 'Editing item' in channel.unread
    session.process_message("")
    assert 'Please enter a number.' in channel.unread
    session.process_message("adas")
    assert 'Please enter a number.' in channel.unread
    session.process_message("4")
    assert 'Please enter the value of one of the options.' in channel.unread

    # Item name
    session.process_message("1")
    assert 'Enter the new name' in channel.unread
    session.process_message("A"*(ITEM_NAME_MAX_LENGTH+1))
    assert "Can't be longer than" in channel.unread
    session.process_message("")
    assert strings.is_empty in channel.unread

    # Item description
    session.process_message("/")
    session.process_message("edit toroid")
    session.process_message("2")
    assert 'Enter the new description' in channel.unread
    session.process_message("")
    session.process_message("A"*(ITEM_DESCRIPTION_MAX_LENGTH+1))
    assert "Can't be longer than" in channel.unread

    # Item visibility
    session.process_message("/")
    session.process_message("edit toroid")
    session.process_message("3")
    assert 'Choose the new visibility' in channel.unread
    session.process_message("")
    assert "It can't be empty, try with another one" in channel.unread
    session.process_message("asdas")
    assert "Please enter the value of one of the options." in channel.unread

