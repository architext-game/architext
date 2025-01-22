from typing import Callable
from architext.chatbot.adapters.fake_sender import FakeSender
from architext.chatbot.adapters.stdout_logger import StdOutLogger
from architext.chatbot.session import Session
from architext.core.adapters.fake_uow import FakeUnitOfWork
from architext.core.domain.entities.world import DEFAULT_WORLD
from architext.core import Architext
from architext.core.messagebus import MessageBus
from architext.core.commands import CreateInitialData
import pytest # type: ignore
from architext.core.domain.entities.user import User
from architext.core.domain.entities.room import Room

from test.fixtures import createTestData


@pytest.fixture
def session_factory() -> Callable[[str], Session]:
    def factory(user_id: str):
        return Session(architext=createTestData(), sender=FakeSender(), logger=StdOutLogger(), user_id=user_id) 
    return factory

def test_build(session_factory: Callable[[str], Session]):
    session = session_factory("oliver")

    session.process_message("build")
    session.process_message("Living Room")
    session.process_message("A cozy living room")
    session.process_message("Door to living room")
    session.process_message("Door to kitchen")
    session.process_message("adadasdas")

    assert isinstance(session.sender, FakeSender)
    sender: FakeSender = session.sender

    sent_text = '\n'.join([message.text for message in sender._sent])
    print(sent_text)

    uow = session.architext._uow
    new_room = next((room for room in uow.rooms.list_rooms() if room.name == "Living Room"), None)
    old_room = uow.rooms.get_room_by_id("olivers")
    assert new_room is not None
    assert old_room is not None
    assert new_room.name == "Living Room"
    assert new_room.description == "A cozy living room"
    assert next(exit for exit in new_room.exits if exit.name == "Door to kitchen").destination_room_id == old_room.id
    assert next(exit for exit in old_room.exits if exit.name == "Door to living room").destination_room_id == new_room.id
    assert "I don't understand that." in sent_text  # check if "adadasdas" was processed as a new command


def test_build_by_unauthorized_user(session_factory: Callable[[str], Session]):
    session = session_factory("alice")

    session.process_message("build")
    session.process_message("afafdadsdfa")
    assert isinstance(session.sender, FakeSender)
    sender: FakeSender = session.sender

    sent_text = '\n'.join([message.text for message in sender._sent])
    print(sent_text)
    assert "You can't build in a world you don't own." in sent_text
    assert "I don't understand that." in sent_text
