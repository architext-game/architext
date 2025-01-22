from architext.core.adapters.fake_uow import FakeUnitOfWork
from architext.core.commands import CreateInitialData, ImportWorld
from architext.core.domain.entities.exit import Exit
from architext.core.domain.entities.user import User
from architext.core.domain.entities.world import World
from architext.core.queries.world_to_text import WorldToText
import pytest # type: ignore
from architext.core.domain.entities.room import Room
from architext.core import Architext

def createTestData() -> Architext:
    uow = FakeUnitOfWork()
    architext = Architext(uow)
    architext.handle(CreateInitialData())

    rabbithole_world = World(
        id="rabbithole",
        name="Down The Rabbit Hole",
        description="A magical place.",
        initial_room_id="rabbitholeroom",
        owner_user_id="rabbit"
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
        owner_user_id="oliver"
    )
    space = Room(
        id="space",
        name="Space",
        description="You are floating in the vastness of the universe, alone.",
        world_id="outer",
        exits=[
            Exit(name="To the spaceship", destination_room_id="spaceship", description="What a nice exit")
        ],
    )
    spaceship = Room(
        id="spaceship",
        name="A Cozy Spaceship",
        description="A cozy Spaceship",
        exits=[
            Exit(name="To Oliver's Room", destination_room_id="olivers", description="A nice smell comes from there"),
            Exit(name="To Alice's Room", destination_room_id="alices", description="A nice smell comes from there"),
            Exit(name="To Bob's Room", destination_room_id="bobs", description="A nice smell comes from there"),
            Exit(name="To Space", destination_room_id="outerroom", description="To the cold cold emptyness"),
        ],
        world_id="outer"
    )
    olivers = Room(
        id="olivers",
        name="Oliver's Room",
        description="This is Oliver's Room",
        exits=[
            Exit(name="To the spaceship", destination_room_id="spaceship", description="What a nice exit"),
            Exit(name="To Alice's Room", destination_room_id="alices", description="A nice smell comes from there"),
            Exit(name="To Bob's Room", destination_room_id="bobs", description="A nice smell comes from there"),
        ],
        world_id="outer"
    )
    alices = Room(
        id="alices",
        name="Alice's Room",
        description="This is Alice's Room",
        exits=[
            Exit(name="To the spaceship", destination_room_id="spaceship", description="What a nice exit"),
            Exit(name="To Oliver's Room", destination_room_id="olivers", description="A nice smell comes from there"),
            Exit(name="To Bob's Room", destination_room_id="bobs", description="A nice smell comes from there"),
        ],
        world_id="outer"
    )
    bobs = Room(
        id="bobs",
        name="Bob's Room",
        description="This is Bob's Room",
        exits=[
            Exit(name="To the spaceship", destination_room_id="spaceship", description="What a nice exit"),
            Exit(name="To Oliver's Room", destination_room_id="olivers", description="A nice smell comes from there"),
            Exit(name="To Alice's Room", destination_room_id="alices", description="A nice smell comes from there"),
        ],
        world_id="outer"
    )

    oliver = User(
        id="oliver",
        name="Oliver",
        email="oliver@example.com",
        room_id="olivers",
        password_hash=b"asdasd"
    )
    alice = User(
        id="alice",
        name="Alice",
        email="alice@example.com",
        room_id="alices",
        password_hash=b"asdasd"
    )
    bob = User(
        id="bob",
        name="Bob",
        email="bob@example.com",
        room_id="bobs",
        password_hash=b"asdasd"
    )
    charlie = User(
        id="bob",
        name="Bob",
        email="bob@example.com",
        room_id=None,
        password_hash=b"asdasd"
    )
    rabbit = User(
        id="rabbit",
        name="Rabbit",
        email="rabbit@example.com",
        room_id="rabbitholeroom",
        password_hash=b"asdasd"
    )
    uow.worlds.save_world(rabbithole_world)
    uow.worlds.save_world(outer_world)
    uow.rooms.save_room(rabbithole_room)
    uow.rooms.save_room(space)
    uow.rooms.save_room(spaceship)
    uow.rooms.save_room(olivers)
    uow.rooms.save_room(alices)
    uow.rooms.save_room(bobs)
    uow.users.save_user(oliver)
    uow.users.save_user(alice)
    uow.users.save_user(bob)
    uow.users.save_user(charlie)
    uow.users.save_user(rabbit)
    return Architext(uow)