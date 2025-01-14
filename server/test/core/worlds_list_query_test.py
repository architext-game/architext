from typing import cast
from unittest.mock import Mock
from architext.core.adapters.fake_notificator import FakeNotificator
from architext.core.adapters.fake_uow import FakeUnitOfWork
from architext.core.commands import TraverseExit, TraverseExitResult, CreateInitialData, CreateConnectedRoom, CreateUser
from architext.core.domain.entities.world import DEFAULT_WORLD, World
from architext.core.queries import ListWorlds
import pytest # type: ignore
from architext.core.domain.entities.user import User
from architext.core.domain.entities.room import Room
from architext.core.domain.entities.exit import Exit
from architext.core.domain.events import UserChangedRoom
from architext.core.messagebus import MessageBus
from architext.core import Architext


@pytest.fixture
def architext() -> Architext:
    uow = FakeUnitOfWork()
    architext = Architext(uow)
    architext.handle(CreateInitialData())
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
    uow.worlds.save_world(rabbithole_world)
    uow.worlds.save_world(outer_world)
    uow.rooms.save_room(rabbithole_room)
    uow.rooms.save_room(outer_room)
    return Architext(uow)


def test_list_worlds(architext: Architext):
    out = architext.query(ListWorlds())
    print(out)
    assert len(out.worlds) == 3
    outer = next((world for world in out.worlds if world.id == "outer"), None)
    assert outer is not None
    assert outer.id == "outer"
    assert outer.description == "Let's explore the universe!"
