from unittest.mock import Mock
from architext.core.adapters.fake_uow import FakeUnitOfWork
from architext.core.commands import EnterWorld, TraverseExit, TraverseExitResult, CreateInitialData, CreateConnectedRoom, CreateUser
from architext.core.domain.entities.world import DEFAULT_WORLD
from architext.core import Architext
import pytest # type: ignore
from architext.core.domain.entities.user import User
from architext.core.domain.entities.room import Room
from architext.core.domain.entities.exit import Exit
from architext.core.domain.entities.world import World
from architext.core.domain.events import UserChangedRoom
from architext.core.messagebus import MessageBus


@pytest.fixture
def architext() -> Architext:
    uow = FakeUnitOfWork()
    rabbithole_world = World(
        id="rabbithole",
        name="Down The Rabbit Hole",
        description="A magical place.",
        initial_room_id="rabbitholeroom",
        owner_user_id=None
    )
    rabbithole_room = Room(
        id="rabbitholeroom",
        name="A really big room",
        description="It seems you drank something that made you small.",
        world_id="rabbithole"
    )
    outer_world = World(
        id="outer",
        name="Outer Wilds",
        description="Let's explore the universe!",
        initial_room_id="outerroom",
        owner_user_id=None
    )
    outer_room = Room(
        id="outerroom",
        name="Space",
        description="You are floating in the vastness of the universe, alone.",
        world_id="outer"
    )
    oliver = User(
        id="oliver",
        name="Oliver",
        email="oliver@example.com",
        room_id="rabbitholeroom",
        password_hash=b"asdasd"
    )
    rabbit = User(
        id="rabbituser",
        name="Rabbit",
        email="rabbit@example.com",
        room_id="rabbitholeroom",
        password_hash=b"asdasd"
    )
    explorer = User(
        id="explorer",
        name="Feldspar",
        email="feldspar@example.com",
        room_id="outerroom",
        password_hash=b"asdasd"
    )
    uow.worlds.save_world(rabbithole_world)
    uow.worlds.save_world(outer_world)
    uow.rooms.save_room(rabbithole_room)
    uow.rooms.save_room(outer_room)
    uow.users.save_user(oliver)
    uow.users.save_user(rabbit)
    uow.users.save_user(explorer)
    return Architext(uow)

def test_enter_world_success(architext: Architext):
    architext.handle(EnterWorld(world_id="outer"), client_user_id="oliver")

    oliver = architext._uow.users.get_user_by_id("oliver")
    assert oliver is not None
    assert oliver.room_id == "outerroom"
    room = architext._uow.rooms.get_room_by_id(oliver.room_id)
    assert room is not None
    assert room.world_id == "outer"
    world = architext._uow.worlds.get_world_by_id(room.world_id)
    assert world is not None
    assert world.name == "Outer Wilds"


@pytest.mark.skip(reason="TODO")
def test_enter_world_that_does_not_exist(uow: FakeUnitOfWork, message_bus: MessageBus):
    with pytest.raises(ValueError, match="User is not in a room."):
        message_bus.handle(uow, TraverseExit(exit_name="To Kitchen"), client_user_id="not_in_room")


@pytest.mark.skip(reason="TODO")
def test_user_changed_room_event_gets_invoked(uow: FakeUnitOfWork):
    pass

@pytest.mark.skip(reason="TODO")
def test_users_get_notified_if_user_enters_world_in_its_room() -> None:
    pass

@pytest.mark.skip(reason="TODO")
def test_users_get_notified_if_user_leaves_world_from_its_room() -> None:
    pass
