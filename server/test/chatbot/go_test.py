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
        uow.notifier = MultiNotifier(multi_notifier_mapping_factory(
            chatbot=ChatbotNotifier(channel=channel),
            web=FakeNotifier()
        ))
        # uow.notifier = ChatbotNotifier(channel=channel)
        architext = Architext(uow=uow)
        return Session(architext=architext, messaging_channel=channel, logger=StdOutLogger(), user_id=user_id) 
    return factory


def test_go(channel: FakeMessagingChannel, session_factory: Callable[[str], Session]):
    session = session_factory("oliver")
    session.process_message("go alice")

    print(channel.all_to("oliver"))
    assert """Alice's Room
This is Alice's Room

👤 Players here: Oliver, Alice.
⮕ Exits: To the spaceship, To Oliver's Room, To Bob's Room.
""" in channel.all_to("oliver")
    

def test_users_in_room_are_told_other_entered(channel: FakeMessagingChannel, session_factory: Callable[[str], Session]):
    session = session_factory("bob")
    session.process_message("go alice")
    print(channel.all_to("alice"))
    assert "Bob arrives through To Bob's Room" in channel.all_to("alice")


def test_users_in_room_are_told_other_left(channel: FakeMessagingChannel, session_factory: Callable[[str], Session]):
    session = session_factory("bob")
    session.process_message("go alice")
    print(channel.all_to("dave"))
    assert "Bob leaves through To Alice's Room." in channel.all_to("dave")
