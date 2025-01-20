from architext.core.adapters.fake_uow import FakeUnitOfWork
from architext.core.commands import CreateInitialData, CreateTemplate, ImportWorld
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


def create_template_success_test(architext: Architext):
    create_template_result = architext.handle(CreateTemplate(
        name="My new template",
        description="I just made this template",
        base_world_id="outer"
    ), client_user_id="oliver")
    template = architext._uow.world_templates.get_world_template_by_id(create_template_result.template_id)
    assert template is not None
    original_text = architext.query(WorldToText(world_id="outer", format="encoded"), client_user_id="oliver").text_representation
    assert template.world_encoded_json == original_text
    assert template.author_id == "oliver"
    assert template.name == "My new template"
    assert template.description == "I just made this template"


    
    