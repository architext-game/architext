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
                    "destination_room_id": "space"
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
    assert out.text_representation == """eJzlVU1v2zAM/SusL70E/QG7ubvssKHAEqwYhqKQbaYmJouGKGfNiv73SUqcybHrAkWbHgoHdkBR7/HjUXrI2NIdGaVvjWow+wTZVefQwjXpSrIF/F+vUEpLrSM2we0runMBvG81WwRXI3SGNmgFz8I2MuTI77LMzS1VYYe0qsSwFmziLb8esqOVPoZlbzgi/ckdKE+31qwcmTsgE6k3SpxBEeD1IJQFKM0GLwIU3pPbs/Y0K47ekV5qaicYr2vlQIGhEiEg7F08uQouo/wizOPN4wIGyfXoPXMOn/nvFpYzzDmUI5fpHK50yNZ347sPZhIphi8Nau1BGxRYW25C7hZnEuKIK1lMJuHLtYd7fToVYMdsl1y8PlfBxZjpKdXtZVKyrnYvbFq3DXp7Tg1DJfT1THTwXOtWNQn438DvAlY+HG9VBvLOMVTMFvy3UK620SHXwl620qhQl644/Qh8BM38IKFC46j+k6SFql48ggfgAf1k70/EvcTSokv1kDJ+24LsHKRULULL1YtGJU3q0F4v18M4hEVoLW2Uw7kSfOE/oLvy9zaMDTmfu9f0DgVq5SfpsDlcKWHowv+zdzxz02rsVZ7eH/Pj1B8bx27veACc+pJ6wyMgbU20JI2Zpe3bMnT6QE1541vgxj//ACOYnvk="""
    