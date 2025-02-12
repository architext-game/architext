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
                    "destination_room_id": "spaceship",
                    "visibility": "auto"
                }
            ],
            "items": []
        },
        {
            "id": "spaceship",
            "name": "A Cozy Spaceship",
            "description": "A cozy Spaceship",
            "exits": [
                {
                    "name": "To Oliver's Room",
                    "description": "A nice smell comes from there",
                    "destination_room_id": "olivers",
                    "visibility": "auto"
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
                    "name": "To Space",
                    "description": "To the cold cold emptyness",
                    "destination_room_id": "space",
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
                    "name": "To the spaceship",
                    "description": "What a nice exit",
                    "destination_room_id": "spaceship",
                    "visibility": "auto"
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
                    "name": "Visible door to bathroom",
                    "description": "A bad smell comes from there",
                    "destination_room_id": "oliversbathroom",
                    "visibility": "unlisted"
                },
                {
                    "name": "Auto door to bathroom",
                    "description": "A bad smell comes from there",
                    "destination_room_id": "oliversbathroom",
                    "visibility": "auto"
                },
                {
                    "name": "Secret exit",
                    "description": "My secret scape pod",
                    "destination_room_id": "space",
                    "visibility": "hidden"
                }
            ],
            "items": [
                {
                    "name": "A cube",
                    "description": "a nice cube",
                    "visibility": "auto"
                },
                {
                    "name": "A small cube",
                    "description": "a nice small cube",
                    "visibility": "auto"
                },
                {
                    "name": "A pyramid",
                    "description": "a nice pyramid",
                    "visibility": "hidden"
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
                    "name": "To the spaceship",
                    "description": "What a nice exit",
                    "destination_room_id": "spaceship",
                    "visibility": "auto"
                },
                {
                    "name": "To Oliver's Room",
                    "description": "A nice smell comes from there",
                    "destination_room_id": "olivers",
                    "visibility": "auto"
                },
                {
                    "name": "To Bob's Room",
                    "description": "A nice smell comes from there",
                    "destination_room_id": "bobs",
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
                    "name": "To the spaceship",
                    "description": "What a nice exit",
                    "destination_room_id": "spaceship",
                    "visibility": "auto"
                },
                {
                    "name": "To Oliver's Room",
                    "description": "A nice smell comes from there",
                    "destination_room_id": "olivers",
                    "visibility": "auto"
                },
                {
                    "name": "To Alice's Room",
                    "description": "A nice smell comes from there",
                    "destination_room_id": "alices",
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
    assert out.text_representation == """eJztVsFu2zAM/RXWl16CfsBu3i47bCiwBCuKIShkm6mJyaIhyVm9Iv8+yYkc27GddiiKHAoESSBSj4/iI6XniDU9khLyQYkCo08Q3VYWNdyRzEy0gKM9Q5NqKi2x8m7f0F4bwKdSskawOUKlaIva4JXfRoosuV2auXigzO8wpUjR2/yacSu/nqOBJXBYhoVB0HuuQLhwG8nCknoEUk3orTBWoTHAmx6VBQjJCm88FD6RPUQNYVbceDfhTU7lSMS7XFgQoChF8AgHFxdceJeT/ALMlgwlJMnW3iQqy9Fu7c/F4j739W4BvfzDzkAuhi/8t4blDLkY0hOX8TRvpT8QV7Afju8oUpOhKVBKB1qggY3mwh+PxpmcucE1Uxn7FDssYumCvD0J4WFfyuEzJ2/PIOHkpfGnpH3QYsoy239hUdrai/qc5F4tt07R2qY/o49VTgbcp+d3AyvH2K0KBbELCRmzBvebCJvrxiGWhl37mEL4A62SS2nFD2H24//0doknFRylkojsvydFF7hPqlKSjMWsT2xUV+/I6vSolphqtF0Fdnl8r8HsHUwqSoSSs9f3b05ZhmrQwZ0zaTppJPihOYL1XCZxpy+n0fo+5zHLWouCsmnAjsN42gOOZaeGY/xaex9tVE1ORZrnyB3tU+ocmaRd+bQd7aZZOy29EUpNW2FxTsVf+Q/IKv1d+6lK1snXjbw9CuTCDdp2s3/5+Jns/19d3L0/efUcJ2JbkvnRGy6eodvFXSGX8cJ690tkstJhUyA3yyxUue/0UePLeawM6rze/QOfZbhJ"""
    