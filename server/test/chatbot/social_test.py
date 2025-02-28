from typing import Callable
from architext.chatbot.adapters.chatbot_notifier import ChatbotNotifier
from architext.chatbot.adapters.fake_messaging_channel import FakeMessagingChannel
from architext.chatbot.ports.messaging_channel import Message, MessageOptions
from architext.chatbot.session import Session
from architext.core.adapters.fake_notifier import FakeNotifier
from architext.core.adapters.multi_notifier import MultiNotifier, multi_notifier_mapping_factory
import pytest # type: ignore


@pytest.fixture
def channel() -> FakeMessagingChannel:
    channel = FakeMessagingChannel()
    channel.send(message=Message(text="asdas", options=MessageOptions()), user_id='patato')
    return channel

@pytest.fixture
def fixed_session_factory(channel: FakeMessagingChannel, session_factory: Callable[[str], Session]) -> Callable[[str], Session]:
    def factory(user_id: str):
        session = session_factory(user_id)
        session.architext._uow._notifier =  MultiNotifier(multi_notifier_mapping_factory(
            chatbot=ChatbotNotifier(channel=channel),
            web=FakeNotifier()
        ))
        return session
    return factory

def test_say(channel: FakeMessagingChannel, fixed_session_factory: Callable[[str], Session]):
    session = fixed_session_factory("bob")
    session.process_message("say I love you dave")

    print(channel.all_to("dave"))
    assert "Bob says \"I love you dave\"" in channel.all_to("dave")


def test_emote(channel: FakeMessagingChannel, fixed_session_factory: Callable[[str], Session]):
    session = fixed_session_factory("bob")
    session.process_message("me winks to dave")

    print(channel.all_to("dave"))
    assert "Bob winks to dave" in channel.all_to("dave")
