import json
from architext.core.adapters.fake_uow import FakeUnitOfWork
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
            "id": "spaceship",
            "name": "A Cozy Spaceship",
            "description": "A cozy Spaceship",
            "exits": [
                {
                    "name": "To Alice's Room",
                    "description": "A nice smell comes from there",
                    "destination_room_id": "alices",
                    "visibility": "auto"
                },
                {
                    "name": "To Bob's Room",
                    "description": "A nice smell comes from there",
                    "destination_room_id": "bobs",
                    "visibility": "auto"
                },
                {
                    "name": "To Oliver's Room",
                    "description": "A nice smell comes from there",
                    "destination_room_id": "olivers",
                    "visibility": "auto"
                },
                {
                    "name": "To Space",
                    "description": "To the cold cold emptyness",
                    "destination_room_id": "space",
                    "visibility": "auto"
                }
            ],
            "items": []
        },
        {
            "id": "oliversbathroom",
            "name": "The Oliver's room private bathroom",
            "description": "How lucky is it that Oliver has a bathroom in his room!",
            "exits": [
                {
                    "name": "To Oliver's Room",
                    "description": "A nice smell comes from there",
                    "destination_room_id": "olivers",
                    "visibility": "auto"
                }
            ],
            "items": []
        },
        {
            "id": "alices",
            "name": "Alice's Room",
            "description": "This is Alice's Room",
            "exits": [
                {
                    "name": "To Bob's Room",
                    "description": "A nice smell comes from there",
                    "destination_room_id": "bobs",
                    "visibility": "auto"
                },
                {
                    "name": "To Oliver's Room",
                    "description": "A nice smell comes from there",
                    "destination_room_id": "olivers",
                    "visibility": "auto"
                },
                {
                    "name": "To the spaceship",
                    "description": "What a nice exit",
                    "destination_room_id": "spaceship",
                    "visibility": "auto"
                }
            ],
            "items": []
        },
        {
            "id": "bobs",
            "name": "Bob's Room",
            "description": "This is Bob's Room",
            "exits": [
                {
                    "name": "To Alice's Room",
                    "description": "A nice smell comes from there",
                    "destination_room_id": "alices",
                    "visibility": "auto"
                },
                {
                    "name": "To Oliver's Room",
                    "description": "A nice smell comes from there",
                    "destination_room_id": "olivers",
                    "visibility": "auto"
                },
                {
                    "name": "To the spaceship",
                    "description": "What a nice exit",
                    "destination_room_id": "spaceship",
                    "visibility": "auto"
                }
            ],
            "items": []
        },
        {
            "id": "olivers",
            "name": "Oliver's Room",
            "description": "This is Oliver's Room. The is an Auto door to bathroom. Also a small cube.",
            "exits": [
                {
                    "name": "Auto door to bathroom",
                    "description": "A bad smell comes from there",
                    "destination_room_id": "oliversbathroom",
                    "visibility": "auto"
                },
                {
                    "name": "Visible door to bathroom",
                    "description": "A bad smell comes from there",
                    "destination_room_id": "oliversbathroom",
                    "visibility": "unlisted"
                },
                {
                    "name": "To Alice's Room",
                    "description": "A nice smell comes from there",
                    "destination_room_id": "alices",
                    "visibility": "auto"
                },
                {
                    "name": "To Bob's Room",
                    "description": "A nice smell comes from there",
                    "destination_room_id": "bobs",
                    "visibility": "auto"
                },
                {
                    "name": "Secret exit",
                    "description": "My secret scape pod",
                    "destination_room_id": "space",
                    "visibility": "hidden"
                },
                {
                    "name": "To the spaceship",
                    "description": "What a nice exit",
                    "destination_room_id": "spaceship",
                    "visibility": "auto"
                }
            ],
            "items": [
                {
                    "name": "A cube",
                    "description": "a nice cube",
                    "visibility": "auto"
                },
                {
                    "name": "A pyramid",
                    "description": "a nice pyramid",
                    "visibility": "hidden"
                },
                {
                    "name": "One pyramid",
                    "description": "a nice pyramid",
                    "visibility": "hidden"
                },
                {
                    "name": "The hidden",
                    "description": "a nice pyramid",
                    "visibility": "hidden"
                },
                {
                    "name": "A small cube",
                    "description": "a nice small cube",
                    "visibility": "auto"
                },
                {
                    "name": "A sphere",
                    "description": "a nice sphere",
                    "visibility": "listed"
                },
                {
                    "name": "A toroid",
                    "description": "a nice toroid",
                    "visibility": "unlisted"
                }
            ]
        },
        {
            "id": "space",
            "name": "Space",
            "description": "You are floating in the vastness of the universe, alone.",
            "exits": [
                {
                    "name": "To the spaceship",
                    "description": "What a nice exit",
                    "destination_room_id": "spaceship",
                    "visibility": "auto"
                }
            ],
            "items": []
        }
    ]
}"""

def test_world_to_encoded_text(architext: Architext):
    out = architext.query(WorldToText(world_id="outer", format="encoded"))
    print(out.text_representation)
    assert out.text_representation == """eJztV01v2zAM/SusL7sE+QG7ebvssCHAUqwYhqCQbaYmJouGJGf1iv73SYntyKk/2iFAcihgxIBIPT6Rj4z8FLGmB1JC3itRYPQRolVlUcMdycxECzjaMzSpptISK+/2Fe0HA/hYStYINkeoFO1QG7zx20iRJbdLMxf3lPkdphQpeptfM27l11MUWExOpbe2PGL4zH9rWIe2Ew4xpC9c8JFsA94i3TLEklJ0fL+70INAytnBFCilwyzQwFZz4Y+lsfG3LgvePzyS8LD7NO3IUEKSbL1fryxHzwvocfjEyfkZJJy8Nv5K+vqcnwLvcV/LYt2q4CS6M3kRpSyzww8Wpa0VGjMRupPUUOCNl6HFg9Q2ex49womwuW5S0RF0FLo8eSOUmnbCIoTeJ9S/8B+QVfq7BjJA1p1D2AYFcmFAdJuBFOR0QL4ZV+uFKjWasKPMu+ac7qdbf0j3nLoNH/e9MVr1m4lhd+dVJQ5UfB7n2qKFeVOl26y1vCZL01a573S9A/i9zqcjMCz1XHbaavf8luAnplsVCmIXEjJmDe7dTrylq7xhdx5TCJ/VKsHliEoG9w+WKRHZf1cpBJ6r1g9vl3hJUpWSZCxmL2R0DQ110cG9xlSjDVskjP6tBnNwMKkoEUrO3n6PyCnLUF1PBwe9su+kgdhN2NY6l8QYylqLgrJxqMBhPjsrhWdG9POlWT8PYByMonHIvs98Gk0ZyHoIr7P3sYa6O3azRvNUBo/2sWkRDvtO3V3rjNzBf3IFwn3NbSU7paoHf131Yt8JY/1NHHjb+9JbgJCsRgf6Zf/sNs//AAOq7ZA="""