from typing import cast
import pytest # type: ignore
from architext.core.adapters.fake_uow import FakeUnitOfWork
from architext.core.messagebus import MessageBus
from architext.core.services.create_connected_room import CreateConnectedRoom, CreateConnectedRoomResult
from architext.core.services.create_initial_data import CreateInitialData
from architext.core.commands import CreateConnectedRoom, CreateWorld
from architext.core import Architext

from architext.core.domain.entities.room import Room
from architext.core.domain.entities.user import User
from architext.core.domain.entities.world import DEFAULT_WORLD


@pytest.fixture
def architext() -> Architext:
    uow = FakeUnitOfWork()
    MessageBus().handle(uow, CreateInitialData())
    uow.rooms.save_room(Room(id="kitchen", name="The Kitchen", description="A beautiful kitchen.", exits=[], world_id=DEFAULT_WORLD.id))
    uow.users.save_user(User(name="Oliver", email="asds@asdsa.com", id="0", room_id="kitchen", password_hash=b"adasd"))
    uow.committed = False
    return Architext(uow)


def test_create_connected_room_success(architext: Architext):
    command = CreateWorld(
        name="My new World",
        description="I like this world",
    )
    out = architext.handle(command, client_user_id="0")

    assert cast(FakeUnitOfWork, architext._uow).committed
    new_world = architext._uow.worlds.get_world_by_id(out.world_id)
    assert new_world is not None
    assert new_world.name == "My new World"
    assert new_world.description == "I like this world"
    default_room = architext._uow.rooms.get_room_by_id(new_world.initial_room_id)
    assert default_room is not None
    assert default_room.world_id == new_world.id
