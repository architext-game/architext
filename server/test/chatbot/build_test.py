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


@pytest.fixture
def session() -> Session:
    uow = FakeUnitOfWork()
    MessageBus().handle(uow, CreateInitialData())
    uow.rooms.save_room(Room(id="kitchen", name="The Kitchen", description="A beautiful kitchen.", exits=[], world_id=DEFAULT_WORLD.id))
    uow.users.save_user(User(name="Oliver", email="asds@asdsa.com", id="0", room_id="kitchen", password_hash=b"adasd"))
    uow.committed = False

    return Session(architext=Architext(uow=uow), sender=FakeSender(), logger=StdOutLogger(), user_id="0") 

def test_build(session: Session):
    session.process_message("build")
    session.process_message("Living Room")
    session.process_message("A cozy living room")
    session.process_message("Door to living room")
    session.process_message("Door to kitchen")
    assert isinstance(session.sender, FakeSender)
    sender: FakeSender = session.sender

    sent_text = '\n'.join([message.text for message in sender._sent])
    print(sent_text)

    uow = session.architext._uow
    new_room = uow.rooms.list_rooms()[2]
    old_room = uow.rooms.get_room_by_id("kitchen")
    assert new_room is not None
    assert old_room is not None
    assert new_room.name == "Living Room"
    assert new_room.description == "A cozy living room"
    assert next(exit for exit in new_room.exits if exit.name == "Door to kitchen").destination_room_id == old_room.id
    assert next(exit for exit in old_room.exits if exit.name == "Door to living room").destination_room_id == new_room.id
