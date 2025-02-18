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
                    "name": "One pyramid",
                    "description": "a nice pyramid",
                    "visibility": "hidden"
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
                },
                {
                    "name": "The hidden",
                    "description": "a nice pyramid",
                    "visibility": "hidden"
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
    assert out.text_representation == """eJztVsFu2zAM/RXWl12CfsBu3i47bCiwBCuGIShkm6mJyqIhyVm9Iv8+0YkTO3GctAiKHAoESSBSfI/io6iXiC09klH6wagCo88Q3VUeLdyTzlw0gZ09Q5daKj2xEbfv6D85wOdSs0XwOUJlaInW4Y1sI0Oewi7LXDxQJjtcqVIUm6y5sPLnJdqztBym7cIe6G+uQAW4hWblyTwCmQZ6qZw36BzwokdlAkqzwVsJhc/kN6gtzIwb7wbe5VQOIN7nyoMCQymCRNi4BHAlLgf5tWGW5CghTb4Wk6o8R6u5nIvHde7z1QR6+bc7W3IxfOV/NUxHyMWQHrgMp3mn5UBCwX4GvoORmgxdgVqHoAU6WFgu5HgsjuTMTVx3LGNJscMi1gHk8iSUhD2XwxdOLs8g4eRc/GPS3mgxZZ2tv7AofS2iPiW5V8utU7Rt05/QxywnB+HT87uFWWAcVpWBOEBCxmwh/CbK57ZxiLXj0D6uUHKgVXItrfghzD7+L7FrPKjgIJVEZW++KbqB+6Qqo8l5zPrEBnX1jqwOj2qKqUXfVWCXx48a3NrBpapEKDl7ff/mlGVo9jq4cyZNJw2Ab5qjtZ7KJO705fFofZ9TMe9MyLm2qqDseMiOw3DifZaXjufKjiqGMt7a+9EG9Rl0aXmM3M5+jt7lRt2wfnu6A5d9V+FdrO2FLkYoLS2Vx7FG+8Z/QVfpUy0XP/nQYeFWXkeBXIVZsN0sjzMZG/L/5uqeJken4+7S3tZ4fDq0s3Hf7eqm3HU8At99zh2tdLupJTfKrK1y3+mjxtfzntqr83z1H9Sw7ZA="""
    