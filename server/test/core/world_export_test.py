from architext.core.adapters.fake_uow import FakeUnitOfWork
from architext.core.commands import CreateInitialData
from architext.core.domain.entities.exit import Exit
from architext.core.domain.entities.user import User
from architext.core.domain.entities.world import World
from architext.core.queries.world_to_text import WorldToText
import pytest # type: ignore
from architext.core.domain.entities.room import Room
from architext.core import Architext
from test.fixtures import createTestArchitext


@pytest.fixture
def architext() -> Architext:
    return createTestArchitext()


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
            "description": "This is Oliver's Room. The is an Auto door to bathroom. Also a small cube.",
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
    assert out.text_representation == """eJzlVU1v2zAM/SusL7sE/QG7eb3s0KHAEqwYhqKQbaYmJouGKKfNiv73ik6c2bHnAkObHooYSUxR7/HjUXpM2NMdOWNvnakw+QzJVRPQwzXZQpIF/F0vUHJPdSB26naJ4ZMAPtSWPUIoERpHG/SCZ7qNHAWKuzxzdUuF7pDa5KhrapNo+fWYHK10MSw7wxHpT27ARLq1ZRPI3QG5lnpjJDgUAV4PQlmAsezwXKHwgcKetaNZcevd0ktJ9QTjdWkCGHCUIyjC3iWSG3UZ5dfCPN08LWCQXIfeMadwwX+2sJxhTiEfuUzncGU129iN7zGYSaQ2fKnQ2ghaocDac6W5e5xJiFtcSdpkenypjXCvT2cUdsz2hbPX58o4GzP9S3V7meRsi90XVnXYqt7miqdjpO9DNXQ17WnhpfatShKIz8DvHFYxpGg1DtImMBTMHuJvZkLpW4fUCkfpSmW0Nk12+jH4CLr5QUKZxVH9J0kzU/z3GB6AB/STvT8R9xJzj6Gvhz7jty3IzkFyUyPUXLykmslR6Sd1aG+U62EcdBFqTxsTcK4EX/kebJP/3urYUIi5R03vUKA0cZIOm/Va0aHT/2fveO72q7FXef8OmR+n7tg4dnvHA+DUF9UbHgH91rSWXmNmabu2DJ0+UFPe+Ba4iZ9no7ig2Q=="""
    
    