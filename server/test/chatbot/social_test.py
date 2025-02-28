from typing import Callable
from architext.chatbot.adapters.chatbot_notifier import ChatbotNotifier
from architext.chatbot.adapters.fake_messaging_channel import FakeMessagingChannel
from architext.chatbot.ports.messaging_channel import Message, MessageOptions
from architext.chatbot.adapters.stdout_logger import StdOutLogger
from architext.chatbot.sender import Sender
from architext.chatbot.session import Session
from architext.core.adapters.fake_notifier import FakeNotifier
from architext.core.adapters.fake_uow import FakeUnitOfWork
from architext.core.adapters.multi_notifier import MultiNotifier, multi_notifier_mapping_factory
from architext.core.domain.entities.world import DEFAULT_WORLD
from architext.core import Architext
import pytest # type: ignore
from architext.core.domain.entities.user import User
from architext.core.domain.entities.room import Room
from architext.core.domain.entities.exit import Exit
from test.fixtures import createTestArchitext, createTestUow

@pytest.fixture
def channel() -> FakeMessagingChannel:
    print("CREATING CHANNEL")
    channel = FakeMessagingChannel()
    channel.send(message=Message(text="asdas", options=MessageOptions()), user_id='patato')
    return channel

@pytest.fixture
def session_factory(channel: FakeMessagingChannel) -> Callable[[str], Session]:
    def factory(user_id: str):
        uow = createTestUow()
        uow._notifier = MultiNotifier(multi_notifier_mapping_factory(
            chatbot=ChatbotNotifier(channel=channel),
            web=FakeNotifier()
        ))
        # uow.notifier = ChatbotNotifier(channel=channel)
        architext = Architext(uow=uow)
        return Session(architext=architext, messaging_channel=channel, logger=StdOutLogger(), user_id=user_id) 
    return factory


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
