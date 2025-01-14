from architext.chatbot.adapters.fake_sender import FakeSender
from architext.chatbot.adapters.stdout_logger import StdOutLogger
from architext.chatbot.session import Session
from architext.core.adapters.fake_uow import FakeUnitOfWork
from architext.core.domain.entities.world import DEFAULT_WORLD
from architext.core import Architext
import pytest # type: ignore
from architext.core.domain.entities.user import User
from architext.core.domain.entities.room import Room


@pytest.fixture
def session() -> Session:
    uow = FakeUnitOfWork()
    uow.rooms.save_room(Room(id="room1", name="Living Room", description="A cozy living room", exits=[], world_id=DEFAULT_WORLD.id))
    uow.rooms.save_room(Room(id="room2", name="Kitchen", description="A modern kitchen", exits=[], world_id=DEFAULT_WORLD.id))
    uow.users.save_user(User(id="0", name="John", email="john@example.com", room_id="room1", password_hash=b"asdasd"))
    uow.users.save_user(User(id="1", name="Alice", email="alice@example.com", room_id=None, password_hash=b"asdasd"))
    uow.users.save_user(User(id="2", name="Paul", email="paul@example.com", room_id="room1", password_hash=b"asdasd"))
    uow.users.save_user(User(id="3", name="Brian", email="brian@example.com", room_id="room2", password_hash=b"asdasd"))

    return Session(architext=Architext(uow=uow), sender=FakeSender(), logger=StdOutLogger(), user_id="0") 

def test_look_room(session: Session):
    session.process_message("look")
    assert isinstance(session.sender, FakeSender)
    sender: FakeSender = session.sender

    sent_text = '\n'.join([message.text for message in sender._sent])
    print(sent_text)
    assert 'Living Room' in sent_text
    assert 'A cozy living room' in sent_text
    assert 'Players here: John, Paul' in sent_text
    assert 'Brian' not in sent_text
    assert 'Alice' not in sent_text
    assert 'Kitchen' not in sent_text
