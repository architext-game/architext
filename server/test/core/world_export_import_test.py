from architext.core.adapters.fake_uow import FakeUnitOfWork
from architext.core.commands import CreateInitialData, ImportWorld
from architext.core.domain.entities.exit import Exit
from architext.core.domain.entities.user import User
from architext.core.domain.entities.world import World
from architext.core.queries.world_to_text import WorldToText
import pytest # type: ignore
from architext.core.domain.entities.room import Room
from architext.core import Architext


@pytest.fixture
def architext() -> Architext:
    uow = FakeUnitOfWork()
    architext = Architext(uow)
    architext.handle(CreateInitialData())
    oliver = User(
        id="oliver",
        name="Oliver",
        email="oliver@example.com",
        room_id="rabbithole",
        password_hash=b"asdasd"
    )
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
        owner_user_id="oliver"
    )
    outer_room = Room(
        id="outerroom",
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
            Exit(name="To Kitchen", destination_room_id="kitchen", description="A nice smell comes from there"),
            Exit(name="To Space", destination_room_id="outerroom", description="To the cold cold emptyness"),
        ],
        world_id="outer"
    )
    kitchen = Room(
        id="kitchen",
        name="Kitchen",
        description="A modern kitchen",
        exits=[],
        world_id="outer"
    )
    uow.users.save_user(oliver)
    uow.worlds.save_world(rabbithole_world)
    uow.worlds.save_world(outer_world)
    uow.rooms.save_room(rabbithole_room)
    uow.rooms.save_room(outer_room)
    uow.rooms.save_room(spaceship)
    uow.rooms.save_room(kitchen)
    return Architext(uow)


def test_world_to_plain_text(architext: Architext):
    out = architext.query(WorldToText(world_id="outer", format="plain"))
    print(out.text_representation)
    assert out.text_representation == """{
    "original_name": "Outer Wilds",
    "original_description": "Let's explore the universe!",
    "initial_room_id": "outerroom",
    "rooms": [
        {
            "id": "outerroom",
            "name": "Space",
            "description": "You are floating in the vastness of the universe, alone.",
            "exits": [
                {
                    "name": "To the spaceship",
                    "description": "What a nice exit",
                    "destination_room_id": "spaceship"
                }
            ]
        },
        {
            "id": "spaceship",
            "name": "A Cozy Spaceship",
            "description": "A cozy Spaceship",
            "exits": [
                {
                    "name": "To Kitchen",
                    "description": "A nice smell comes from there",
                    "destination_room_id": "kitchen"
                },
                {
                    "name": "To Space",
                    "description": "To the cold cold emptyness",
                    "destination_room_id": "outerroom"
                }
            ]
        },
        {
            "id": "kitchen",
            "name": "Kitchen",
            "description": "A modern kitchen",
            "exits": []
        }
    ]
}"""

def test_world_to_encoded_text(architext: Architext):
    out = architext.query(WorldToText(world_id="outer", format="encoded"))
    print(out.text_representation)
    assert out.text_representation == """eJx9kcFOwzAMhl/F9MKl4gG4TRxB4jCkCaFpilp3tZbEVZxOG9Penbi0tIPSS6LE9v/5ty8ZB9qTN3bnjcPsEbLXNmKADdlSshzGeIlSBGoisde0F4z3AnhqLAeEWCO0no4YBO+0jDxFSlWB2e2o1ApWYX1rXG9Jvx+XbCY69LJuTIH68Qv+zi2YhK0sm0h+D+S7Fo5GokcR4OqmpRyMZY8PKoUnij15wLxxly1Kk5qaGeKmNhEMeCoQVKFPSXCjKVOfo8x1e81hMHijPpBX8MSfZ1gvkFdQ/EmZ9/BMsajRz2p0jYtDa5OcQ4EqsFPXAResHHrFzsaE9N9e+kEWbMvvA10Tz7qRBci4+Zt5HUY3A3nJoOMSg4dJ1c+Qtkn3C67G+X8="""

def test_import_plain_text_world(architext: Architext):
    text = """{
    "original_name": "Outer Wilds",
    "original_description": "Let's explore the universe!",
    "initial_room_id": "outerroom",
    "rooms": [
        {
            "id": "outerroom",
            "name": "Space",
            "description": "You are floating in the vastness of the universe, alone.",
            "exits": [
                {
                    "name": "To the spaceship",
                    "description": "What a nice exit",
                    "destination_room_id": "spaceship"
                }
            ]
        },
        {
            "id": "spaceship",
            "name": "A Cozy Spaceship",
            "description": "A cozy Spaceship",
            "exits": [
                {
                    "name": "To Kitchen",
                    "description": "A nice smell comes from there",
                    "destination_room_id": "kitchen"
                },
                {
                    "name": "To Space",
                    "description": "To the cold cold emptyness",
                    "destination_room_id": "outerroom"
                }
            ]
        },
        {
            "id": "kitchen",
            "name": "Kitchen",
            "description": "A modern kitchen",
            "exits": []
        }
    ]
}"""
    result = architext.handle(ImportWorld(
        name="Imported World",
        description="Tremenda copia de mundo",
        format="plain",
        text_representation=text
    ), client_user_id="oliver")


    
    