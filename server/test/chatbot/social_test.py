from typing import Callable
from architext.chatbot.adapters.fake_messaging_channel import FakeMessagingChannel
from architext.chatbot.session import Session


def test_say(channel: FakeMessagingChannel, session_factory: Callable[[str], Session]):
    session = session_factory("bob")
    session.process_message("say I love you dave")

    print(channel.all_to("dave"))
    assert "Bob says \"I love you dave\"" in channel.all_to("dave")


def test_emote(channel: FakeMessagingChannel, session_factory: Callable[[str], Session]):
    session = session_factory("bob")
    session.process_message("me winks to dave")

    print(channel.all_to("dave"))
    assert "Bob winks to dave" in channel.all_to("dave")
