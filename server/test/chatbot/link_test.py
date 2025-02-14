from typing import Callable
from architext.chatbot import strings
from architext.chatbot.adapters.fake_messaging_channel import FakeMessagingChannel
from architext.chatbot.adapters.stdout_logger import StdOutLogger
from architext.chatbot.session import Session
from architext.core.settings import EXIT_NAME_MAX_LENGTH
import pytest # type: ignore


def test_link_success(channel: FakeMessagingChannel, session_factory: Callable[[str], Session]):
    session = session_factory("oliver")

    session.process_message("link")
    session.process_message("alices")
    session.process_message("The new exit to alices")
    session.process_message("The new exit to olivers")

    sent_text = channel.all
    print(sent_text)

    assert "Your new exits are ready!" in sent_text
    uow = session.architext._uow
    olivers = uow.rooms.get_room_by_id("olivers")
    assert olivers is not None
    alices = uow.rooms.get_room_by_id("alices")
    assert alices is not None
    assert olivers.exits.get("The new exit to alices") is not None
    assert alices.exits.get("The new exit to olivers") is not None


def test_link_with_room_in_other_world_fails(channel: FakeMessagingChannel, session_factory: Callable[[str], Session]):
    session = session_factory("oliver")

    session.process_message("link")
    session.process_message("rabbitholeroom")
    assert strings.room_not_found in channel.unread


def test_link_by_unauthorized_user_fails(channel: FakeMessagingChannel, session_factory: Callable[[str], Session]):
    session = session_factory("alice")
    session.process_message("link")
    assert strings.insufficient_privileges in channel.unread


def test_link_rejects_duplicated_exits(channel: FakeMessagingChannel, session_factory: Callable[[str], Session]):
    session = session_factory("oliver")

    session.process_message("link")
    session.process_message("alices")
    session.process_message("To Alice's Room")
    assert strings.room_name_clash in channel.unread
    session.process_message("")  # there is already an exit with the default name here
    assert strings.room_name_clash in channel.unread

    session.process_message("A proper name")
    assert "Enter the name of the exit in Alice's Room" in channel.unread
    session.process_message("To Oliver's Room")
    assert strings.room_name_clash in channel.unread
    session.process_message("")  # there is already an exit with the default name here
    assert strings.room_name_clash in channel.unread
    session.process_message("A proper name")
    assert "Your new exits are ready!" in channel.unread


def test_link_error_messages(channel: FakeMessagingChannel, session_factory: Callable[[str], Session]):
    session = session_factory("oliver")

    session.process_message("link")
    session.process_message("alices")
    channel.unread
    session.process_message("A"*(EXIT_NAME_MAX_LENGTH+1))
    assert strings.too_long.format(limit=EXIT_NAME_MAX_LENGTH) in channel.unread
    session.process_message("Proper Name")
    session.process_message("A"*(EXIT_NAME_MAX_LENGTH+1))
    assert strings.too_long.format(limit=EXIT_NAME_MAX_LENGTH) in channel.unread
    session.process_message("Proper Name")
    assert "Your new exits are ready!" in channel.unread
