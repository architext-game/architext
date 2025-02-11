from typing import Callable
from architext.chatbot.adapters.fake_messaging_channel import FakeMessagingChannel
from architext.chatbot.adapters.stdout_logger import StdOutLogger
from architext.chatbot.session import Session
import pytest # type: ignore
from test.fixtures import createTestArchitext


@pytest.fixture
def session_factory() -> Callable[[str], Session]:
    def factory(user_id: str):
        architext = createTestArchitext()
        return Session(architext=architext, messaging_channel=FakeMessagingChannel(), logger=StdOutLogger(), user_id=user_id) 
    return factory

def test_raze_success(session_factory: Callable[[str], Session]):
    session = session_factory("oliver")

    session.process_message("raze")
    session.process_message("Oliver's Room")  # you need to confirm by typing the room's name
    session.process_message("adasdsa")  # you need to confirm by typing the room's name

    assert isinstance(session.sender.channel, FakeMessagingChannel)
    sender: FakeMessagingChannel = session.sender.channel
    sent_text = '\n'.join([message.text for message in sender._sent])
    print(sent_text)

    assert 'The room and the exits leading to it have been deleted' in sent_text
    assert 'I don\'t understand that'

    uow = session.architext._uow
    olivers = uow.rooms.get_room_by_id("olivers")
    assert olivers is None


def test_raze_bad_confirmation(session_factory: Callable[[str], Session]):
    session = session_factory("oliver")

    session.process_message("raze")
    session.process_message("Oliver's Roo")  # you need to confirm by typing the room's name
    session.process_message("adasdsa")  # you need to confirm by typing the room's name


    assert isinstance(session.sender.channel, FakeMessagingChannel)
    sender: FakeMessagingChannel = session.sender.channel
    sent_text = '\n'.join([message.text for message in sender._sent])
    print(sent_text)

    assert 'Deletion cancelled' in sent_text
    assert 'I don\'t understand that'

    uow = session.architext._uow
    olivers = uow.rooms.get_room_by_id("olivers")
    assert olivers is not None


def test_unauthorized_user_cannot_raze(session_factory: Callable[[str], Session]):
    session = session_factory("alice")
    session.process_message("raze")
    session.process_message("asdasd")

    assert isinstance(session.sender.channel, FakeMessagingChannel)
    sender: FakeMessagingChannel = session.sender.channel
    sent_text = '\n'.join([message.text for message in sender._sent])
    print(sent_text)

    assert "You don't have enough privileges to do that here." in sent_text
    assert 'I don\'t understand that' in sent_text
