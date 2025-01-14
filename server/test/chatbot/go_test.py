from architext.chatbot.adapters.fake_sender import FakeSender
from architext.chatbot.adapters.stdout_logger import StdOutLogger
from architext.chatbot.session import Session
from architext.core.adapters.fake_uow import FakeUnitOfWork
from architext.core.domain.entities.world import DEFAULT_WORLD
from architext.core.messagebus import MessageBus
import pytest # type: ignore
from architext.core.domain.entities.user import User
from architext.core.domain.entities.room import Room
from architext.core.domain.entities.exit import Exit


@pytest.fixture
def session() -> Session:
    uow = FakeUnitOfWork()
    room1 = Room(
        id="room1",
        name="Living Room",
        description="A cozy living room",
        exits=[
            Exit(name="To Kitchen", destination_room_id="room2", description="")
        ],
        world_id=DEFAULT_WORLD.id
    )
    room2 = Room(
        id="room2",
        name="Kitchen",
        description="A modern kitchen",
        exits=[],
        world_id=DEFAULT_WORLD.id
    )
    user1 = User(
        id="in_room",
        name="UserInRoom",
        email="john@example.com",
        room_id="room1",
        password_hash=b"asdasd"
    )
    user2 = User(
        id="not_in_room",
        name="UserNotInRoom",
        email="Alice@example.com",
        room_id=None,
        password_hash=b"asdasd"
    )
    uow.rooms.save_room(room1)
    uow.rooms.save_room(room2)
    uow.users.save_user(user1)
    uow.users.save_user(user2)

    return Session(uow=uow, sender=FakeSender(), logger=StdOutLogger(), user_id="in_room") 

def test_go(session: Session):
    session.process_message("go To Kitchen")
    assert isinstance(session.sender, FakeSender)
    sender: FakeSender = session.sender

    sent_text = '\n'.join([message.text for message in sender._sent])
    print(sent_text)
    assert sent_text == """Kitchen
A modern kitchen

👤 UserInRoom is here.
"""
