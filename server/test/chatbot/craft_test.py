from typing import Callable
from architext.chatbot import strings
from architext.chatbot.adapters.fake_messaging_channel import FakeMessagingChannel
from architext.chatbot.adapters.stdout_logger import StdOutLogger
from architext.chatbot.session import Session
from architext.core.settings import ITEM_DESCRIPTION_MAX_LENGTH, ITEM_NAME_MAX_LENGTH
import pytest # type: ignore


def test_craft_item_success(channel: FakeMessagingChannel, session_factory: Callable[[str], Session]):
    session = session_factory("oliver")

    session.process_message("craft")
    assert "You start crafting an item" in channel.unread
    session.process_message("A brand new item")
    assert "Description" in channel.unread
    session.process_message("This is the perfect item for everyone")
    assert "Visibility" in channel.unread
    session.process_message("l")
    assert "Your new item is ready" in channel.unread

    uow = session.architext._uow
    olivers = uow.rooms.get_room_by_id("olivers")
    assert olivers is not None
    item = olivers.items.get("A brand new item")
    assert item is not None
    assert item.name == "A brand new item"
    assert item.description == "This is the perfect item for everyone"
    assert item.visibility == 'listed'

def test_craft_hidden_item_success(channel: FakeMessagingChannel, session_factory: Callable[[str], Session]):
    session = session_factory("oliver")

    session.process_message("craft")
    session.process_message("A brand new item")
    session.process_message("This is the perfect item for everyone")
    session.process_message("h")

    uow = session.architext._uow
    olivers = uow.rooms.get_room_by_id("olivers")
    assert olivers is not None
    item = olivers.items.get("A brand new item")
    assert item is not None
    assert item.visibility == 'hidden'
    

def test_craft_error_messages(channel: FakeMessagingChannel, session_factory: Callable[[str], Session]):
    session = session_factory("oliver")

    session.process_message("craft")
    assert "You start crafting an item" in channel.unread

    # Name
    session.process_message("a toroid")
    assert strings.room_name_clash in channel.unread
    session.process_message("")
    assert strings.is_empty in channel.unread
    session.process_message("A"*(ITEM_NAME_MAX_LENGTH+1))
    assert strings.too_long.format(limit=ITEM_NAME_MAX_LENGTH) in channel.unread
    session.process_message("A proper name")
    channel.unread

    # Description
    session.process_message("A"*(ITEM_DESCRIPTION_MAX_LENGTH+1))
    assert strings.too_long.format(limit=ITEM_DESCRIPTION_MAX_LENGTH) in channel.unread
    session.process_message("A proper description")
    channel.unread

    # Visibility
    session.process_message("")
    assert "Please enter the value of one of the options." in channel.unread
    session.process_message("asdas")
    assert "Please enter the value of one of the options." in channel.unread
    session.process_message("h")

    assert "Your new item is ready" in channel.unread

