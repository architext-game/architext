from typing import Callable
from architext.chatbot import strings
from architext.chatbot.adapters.fake_messaging_channel import FakeMessagingChannel
from architext.chatbot.adapters.stdout_logger import StdOutLogger
from architext.chatbot.session import Session
import pytest # type: ignore


def test_delete_item_success(channel: FakeMessagingChannel, session_factory: Callable[[str], Session]):
    session = session_factory("oliver")

    session.process_message("delete A toroid")
    session.process_message("asdasd")

    sent_text = channel.all
    print(sent_text)

    assert 'Item "A toroid" has been deleted' in sent_text
    assert "I don't understand that." in sent_text

    uow = session.architext._uow
    with uow as transaction:
        olivers = transaction.rooms.get_room_by_id("olivers")
        assert olivers is not None
        assert olivers.items.get("A toroid") is None


def test_delete_exit_success(channel: FakeMessagingChannel, session_factory: Callable[[str], Session]):
    session = session_factory("oliver")

    session.process_message("delete To the spaceship")
    session.process_message("asdasd")

    sent_text = channel.all
    print(sent_text)

    assert 'Exit "To the spaceship" has been deleted' in sent_text
    assert "I don't understand that." in sent_text

    uow = session.architext._uow
    with uow as transaction:
        olivers = transaction.rooms.get_room_by_id("olivers")
        assert olivers is not None
        assert olivers.exits.get("To the spaceship") is None


def test_unauthorized_user_cannot_delete(channel: FakeMessagingChannel, session_factory: Callable[[str], Session]):
    session = session_factory("alice")

    session.process_message("delete To Oliver's Room")
    assert strings.insufficient_privileges in channel.all_to("alice")


def test_non_exact_name_for_delete_fails(channel: FakeMessagingChannel, session_factory: Callable[[str], Session]):
    session = session_factory("oliver")

    session.process_message("delete To Oliver's Roo")
    assert "There is not any exit or item called" in channel.all_to("oliver")


def test_delete_with_empty_name_fails(channel: FakeMessagingChannel, session_factory: Callable[[str], Session]):
    session = session_factory("oliver")

    session.process_message("delete ")
    assert "I don't understand that" in channel.all_to("oliver")
