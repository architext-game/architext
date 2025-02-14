from typing import Callable
from architext.chatbot import strings
from architext.chatbot.adapters.fake_messaging_channel import FakeMessagingChannel
from architext.chatbot.session import Session

# The logic to match names with things is thorougly tested
# in the tests for the GetThingInRoom query.

def test_look_at_item_shows_description(channel: FakeMessagingChannel, session_factory: Callable[[str], Session]):
    session = session_factory("oliver")

    session.process_message("look toroid")
    assert "a nice toroid" in channel.unread


def test_look_at_exit_shows_description(channel: FakeMessagingChannel, session_factory: Callable[[str], Session]):
    session = session_factory("oliver")
    
    session.process_message("look alice's")
    assert "A nice smell comes from there" in channel.unread


def test_look_at_not_found_item(channel: FakeMessagingChannel, session_factory: Callable[[str], Session]):
    session = session_factory("oliver")

    session.process_message("look adasdasd")
    assert strings.not_found in channel.unread


def test_look_at_ambiguous_target(channel: FakeMessagingChannel, session_factory: Callable[[str], Session]):
    session = session_factory("oliver")

    session.process_message("look room")
    assert strings.many_found in channel.unread

