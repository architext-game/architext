from architext.core.adapters.fake_uow import FakeUnitOfWork
from architext.core.commands import CreateInitialData
from architext.core.domain.entities.exit import Exit
from architext.core.domain.entities.user import User
from architext.core.domain.entities.world import World
from architext.core.queries.world_to_text import WorldToText
import pytest # type: ignore
from architext.core.domain.entities.room import Room
from architext.core import Architext
from test.fixtures import createTestData


@pytest.fixture
def architext() -> Architext:
    return createTestData()


def test_world_to_plain_text(architext: Architext):
    out = architext.query(WorldToText(world_id="outer", format="plain"))
    print(out.text_representation)
    assert out.text_representation == """{
    "original_name": "Outer Wilds",
    "original_description": "Let's explore the universe!",
    "initial_room_id": "space",
    "rooms": [
        {
            "id": "space",
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
                    "name": "To Oliver's Room",
                    "description": "A nice smell comes from there",
                    "destination_room_id": "olivers"
                },
                {
                    "name": "To Alice's Room",
                    "description": "A nice smell comes from there",
                    "destination_room_id": "alices"
                },
                {
                    "name": "To Bob's Room",
                    "description": "A nice smell comes from there",
                    "destination_room_id": "bobs"
                },
                {
                    "name": "To Space",
                    "description": "To the cold cold emptyness",
                    "destination_room_id": "outerroom"
                }
            ]
        },
        {
            "id": "olivers",
            "name": "Oliver's Room",
            "description": "This is Oliver's Room. The is an Auto door to bathroom.",
            "exits": [
                {
                    "name": "To the spaceship",
                    "description": "What a nice exit",
                    "destination_room_id": "spaceship"
                },
                {
                    "name": "To Alice's Room",
                    "description": "A nice smell comes from there",
                    "destination_room_id": "alices"
                },
                {
                    "name": "To Bob's Room",
                    "description": "A nice smell comes from there",
                    "destination_room_id": "bobs"
                },
                {
                    "name": "Visible door to bathroom",
                    "description": "A bad smell comes from there",
                    "destination_room_id": "oliversbathroom"
                },
                {
                    "name": "Auto door to bathroom",
                    "description": "A bad smell comes from there",
                    "destination_room_id": "oliversbathroom"
                },
                {
                    "name": "Secret exit",
                    "description": "My secret scape pod",
                    "destination_room_id": "space"
                }
            ]
        },
        {
            "id": "oliversbathroom",
            "name": "The Oliver's room private bathroom",
            "description": "How lucky is it that Oliver has a bathroom in his room!",
            "exits": [
                {
                    "name": "To Oliver's Room",
                    "description": "A nice smell comes from there",
                    "destination_room_id": "olivers"
                }
            ]
        },
        {
            "id": "alices",
            "name": "Alice's Room",
            "description": "This is Alice's Room",
            "exits": [
                {
                    "name": "To the spaceship",
                    "description": "What a nice exit",
                    "destination_room_id": "spaceship"
                },
                {
                    "name": "To Oliver's Room",
                    "description": "A nice smell comes from there",
                    "destination_room_id": "olivers"
                },
                {
                    "name": "To Bob's Room",
                    "description": "A nice smell comes from there",
                    "destination_room_id": "bobs"
                }
            ]
        },
        {
            "id": "bobs",
            "name": "Bob's Room",
            "description": "This is Bob's Room",
            "exits": [
                {
                    "name": "To the spaceship",
                    "description": "What a nice exit",
                    "destination_room_id": "spaceship"
                },
                {
                    "name": "To Oliver's Room",
                    "description": "A nice smell comes from there",
                    "destination_room_id": "olivers"
                },
                {
                    "name": "To Alice's Room",
                    "description": "A nice smell comes from there",
                    "destination_room_id": "alices"
                }
            ]
        }
    ]
}"""

def test_world_to_encoded_text(architext: Architext):
    out = architext.query(WorldToText(world_id="outer", format="encoded"))
    print(out.text_representation)
    assert out.text_representation == """eJzlVU1v2zAM/SusL7sE/QG7ZbvssKHAEqwYhqKQbaYmJouGKGfNiv73iU6cybHnAkObHooYSUxR7/HjUXrI2NMdOWNvnakxew/ZVRvQwzXZUrIF/F0vUQpPTSB26vYZwzsBvG8se4RQIbSOtugFL3QbOQoUd3nm+pZK3SGNKVDX1CbR8uMhO1npY1j1hhPS79yCiXQbyyaQuwNyHfXWSHAoArwZhLIAY9nhpULhPYUDa0+z5s67o5eKmgnG68oEMOCoQFCEg0skN+oyyq+Debx5XMAguR69Z17CR/69g9UM8xKKkct0DldWs43d+BqDmUTqwpcarY2gNQpsPNeau8eZhLjDlaxLJuFb2gj3/HRGYcdsHzh/fq6c8zHTv1R3kEnBttx/Yd2Eneptrng6Rvo+VENf00QLT7VvXZFAfAZ+l7COIUWrcbBsA0PJ7CH+5iZUSnt2zb8FkXwjodziqNiTpLkp/3vmjsAD+slGn4l7hYXHkOohZfyyA9k7SGEahIbLp1QzORdpUsf2Rrketa+L0HjamoBzJfjEv8C2xc+dzgiFmHvU9B4FKhPH5rhZ7xCdMP1/8YqHbFqNg8rTC2N+nPoz4tTtFQ+Ac99KL3gEpK3pLEljZmn7tgyd3lBTXvgWuImfPyeEmoM="""


    
    