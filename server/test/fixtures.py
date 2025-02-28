import datetime
from architext.chatbot.adapters.fake_messaging_channel import FakeMessagingChannel
from architext.content.the_monks_riddle import THE_MONKS_RIDDLE_ENCODED
from architext.core.adapters.fake_uow import FakeUnitOfWork
from architext.core.domain.entities.exit import Exit
from architext.core.domain.entities.item import Item
from architext.core.domain.entities.mission import default_missions, MissionLog
from architext.core.domain.entities.user import User, WorldVisitRecord
from architext.core.domain.entities.world import World
from architext.core.domain.entities.world_template import WorldTemplate
from architext.core.domain.entities.room import Room
from architext.core import Architext
from typing import Callable
from architext.chatbot.adapters.chatbot_notifier import ChatbotNotifier
from architext.chatbot.ports.messaging_channel import Message, MessageOptions
from architext.chatbot.adapters.stdout_logger import StdOutLogger
from architext.chatbot.session import Session
from architext.core.adapters.fake_notifier import FakeNotifier
from architext.core.adapters.multi_notifier import MultiNotifier, multi_notifier_mapping_factory
import pytest # type: ignore
from architext.core.adapters.sqlalchemy.uow import SQLAlchemyUnitOfWork
from architext.core.adapters.sqlalchemy.session import db_connection

from architext.core.ports.unit_of_work import UnitOfWork

def add_test_data(uow: UnitOfWork):
    emptytemplate = WorldTemplate(
        id="emptytemplate",
        name="New World",
        description="An Empty World",
        author_id=None,
        world_encoded_json="""eJx9kcFOwzAMhl/F9MKl4gG4TRxB4jCkCaFpilp3tZbEVZxOG9Penbi0tIPSS6LE9v/5ty8ZB9qTN3bnjcPsEbLXNmKADdlSshzGeIlSBGoisde0F4z3AnhqLAeEWCO0no4YBO+0jDxFSlWB2e2o1ApWYX1rXG9Jvx+XbCY69LJuTIH68Qv+zi2YhK0sm0h+D+S7Fo5GokcR4OqmpRyMZY8PKoUnij15wLxxly1Kk5qaGeKmNhEMeCoQVKFPSXCjKVOfo8x1e81hMHijPpBX8MSfZ1gvkFdQ/EmZ9/BMsajRz2p0jYtDa5OcQ4EqsFPXAResHHrFzsaE9N9e+kEWbMvvA10Tz7qRBci4+Zt5HUY3A3nJoOMSg4dJ1c+Qtkn3C67G+X8=""",
        visibility="public"
    )
    monkstemplate = WorldTemplate(
        id="monksriddletemplate",
        name="The Monk's Riddle",
        description="A monastery full of mistery.",
        author_id=None,
        world_encoded_json=THE_MONKS_RIDDLE_ENCODED,
        visibility="public"
    )
    templateforme = WorldTemplate(
        id="templateforme",
        name="A template only for me",
        description="For the new worlds I create",
        author_id="oliver",
        world_encoded_json="""eJx9kcFOwzAMhl/F9MKl4gG4TRxB4jCkCaFpilp3tZbEVZxOG9Penbi0tIPSS6LE9v/5ty8ZB9qTN3bnjcPsEbLXNmKADdlSshzGeIlSBGoisde0F4z3AnhqLAeEWCO0no4YBO+0jDxFSlWB2e2o1ApWYX1rXG9Jvx+XbCY69LJuTIH68Qv+zi2YhK0sm0h+D+S7Fo5GokcR4OqmpRyMZY8PKoUnij15wLxxly1Kk5qaGeKmNhEMeCoQVKFPSXCjKVOfo8x1e81hMHijPpBX8MSfZ1gvkFdQ/EmZ9/BMsajRz2p0jYtDa5OcQ4EqsFPXAResHHrFzsaE9N9e+kEWbMvvA10Tz7qRBci4+Zt5HUY3A3nJoOMSg4dJ1c+Qtkn3C67G+X8=""",
        visibility="private"
    )
    braggingtemplate = WorldTemplate(
        id="braggingtemplate",
        name="A template everyone should see",
        description="To brag about",
        author_id="oliver",
        world_encoded_json="""eJx9kcFOwzAMhl/F9MKl4gG4TRxB4jCkCaFpilp3tZbEVZxOG9Penbi0tIPSS6LE9v/5ty8ZB9qTN3bnjcPsEbLXNmKADdlSshzGeIlSBGoisde0F4z3AnhqLAeEWCO0no4YBO+0jDxFSlWB2e2o1ApWYX1rXG9Jvx+XbCY69LJuTIH68Qv+zi2YhK0sm0h+D+S7Fo5GokcR4OqmpRyMZY8PKoUnij15wLxxly1Kk5qaGeKmNhEMeCoQVKFPSXCjKVOfo8x1e81hMHijPpBX8MSfZ1gvkFdQ/EmZ9/BMsajRz2p0jYtDa5OcQ4EqsFPXAResHHrFzsaE9N9e+kEWbMvvA10Tz7qRBci4+Zt5HUY3A3nJoOMSg4dJ1c+Qtkn3C67G+X8=""",
        visibility="public"
    )
    rabbittemplate = WorldTemplate(
        id="rabbittemplate",
        name="Misterious Template",
        description="This is so misterious",
        author_id="rabbit",
        world_encoded_json="""eJx9kcFOwzAMhl/F9MKl4gG4TRxB4jCkCaFpilp3tZbEVZxOG9Penbi0tIPSS6LE9v/5ty8ZB9qTN3bnjcPsEbLXNmKADdlSshzGeIlSBGoisde0F4z3AnhqLAeEWCO0no4YBO+0jDxFSlWB2e2o1ApWYX1rXG9Jvx+XbCY69LJuTIH68Qv+zi2YhK0sm0h+D+S7Fo5GokcR4OqmpRyMZY8PKoUnij15wLxxly1Kk5qaGeKmNhEMeCoQVKFPSXCjKVOfo8x1e81hMHijPpBX8MSfZ1gvkFdQ/EmZ9/BMsajRz2p0jYtDa5OcQ4EqsFPXAResHHrFzsaE9N9e+kEWbMvvA10Tz7qRBci4+Zt5HUY3A3nJoOMSg4dJ1c+Qtkn3C67G+X8=""",
        visibility="private"
    )

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

    public_tabern = World(
        id="tabern",
        name="Public tabern",
        description="A public tabern",
        initial_room_id="tabern_table",
        owner_user_id=None,
        visibility="public"
    )
    a_table_in_the_tabern = Room(
        id="tabern_table",
        name="A table in the tabern",
        description="It is somewhat dirty",
        world_id="tabern"
    )

    outer_world = World(
        id="outer",
        name="Outer Wilds",
        description="Let's explore the universe!",
        initial_room_id="space",
        owner_user_id="oliver",
        visibility="public"
    )
    space = Room(
        id="space",
        name="Space",
        description="You are floating in the vastness of the universe, alone.",
        world_id="outer",
        exits={
            "To the spaceship": Exit(name="To the spaceship", destination_room_id="spaceship", description="What a nice exit")
        }
    )
    spaceship = Room(
        id="spaceship",
        name="A Cozy Spaceship",
        description="A cozy Spaceship",
        exits={
            "To Oliver's Room": Exit(name="To Oliver's Room", destination_room_id="olivers", description="A nice smell comes from there"),
            "To Alice's Room": Exit(name="To Alice's Room", destination_room_id="alices", description="A nice smell comes from there"),
            "To Bob's Room": Exit(name="To Bob's Room", destination_room_id="bobs", description="A nice smell comes from there"),
            "To Space": Exit(name="To Space", destination_room_id="space", description="To the cold cold emptyness"),
        },
        world_id="outer"
    )
    olivers = Room(
        id="olivers",
        name="Oliver's Room",
        description="This is Oliver's Room. The is an Auto door to bathroom. Also a small cube.",
        exits={
            "To the spaceship": Exit(name="To the spaceship", destination_room_id="spaceship", description="What a nice exit"),
            "To Alice's Room": Exit(name="To Alice's Room", destination_room_id="alices", description="A nice smell comes from there"),
            "To Bob's Room": Exit(name="To Bob's Room", destination_room_id="bobs", description="A nice smell comes from there"),
            "Visible door to bathroom": Exit(name="Visible door to bathroom", destination_room_id="oliversbathroom", description="A bad smell comes from there", visibility="unlisted"),
            "Auto door to bathroom": Exit(name="Auto door to bathroom", destination_room_id="oliversbathroom", description="A bad smell comes from there", visibility="auto"),
            "Secret exit": Exit(name="Secret exit", destination_room_id="space", description="My secret scape pod", visibility="hidden"),
        },
        items={
            "A cube": Item(name="A cube", description="a nice cube", visibility="auto"),
            "A small cube": Item(name="A small cube", description="a nice small cube", visibility="auto"),
            "One pyramid": Item(name="One pyramid", description="a nice pyramid", visibility="hidden"),
            "A pyramid": Item(name="A pyramid", description="a nice pyramid", visibility="hidden"),
            "A sphere": Item(name="A sphere", description="a nice sphere", visibility="listed"),
            "A toroid": Item(name="A toroid", description="a nice toroid", visibility="unlisted"),
            "The hidden": Item(name="The hidden", description="a nice pyramid", visibility="hidden"),
        },
        world_id="outer"
    )
    private_bathroom = Room(
        id="oliversbathroom",
        name="The Oliver's room private bathroom",
        description="How lucky is it that Oliver has a bathroom in his room!",
        exits={
            "To Oliver's Room": Exit(name="To Oliver's Room", destination_room_id="olivers", description="A nice smell comes from there"),
        },
        world_id="outer"
    )
    alices = Room(
        id="alices",
        name="Alice's Room",
        description="This is Alice's Room",
        exits={
            "To the spaceship": Exit(name="To the spaceship", destination_room_id="spaceship", description="What a nice exit"),
            "To Oliver's Room": Exit(name="To Oliver's Room", destination_room_id="olivers", description="A nice smell comes from there"),
            "To Bob's Room": Exit(name="To Bob's Room", destination_room_id="bobs", description="A nice smell comes from there"),
        },
        world_id="outer"
    )
    bobs = Room(
        id="bobs",
        name="Bob's Room",
        description="This is Bob's Room",
        exits={
            "To the spaceship": Exit(name="To the spaceship", destination_room_id="spaceship", description="What a nice exit"),
            "To Oliver's Room": Exit(name="To Oliver's Room", destination_room_id="olivers", description="A nice smell comes from there"),
            "To Alice's Room": Exit(name="To Alice's Room", destination_room_id="alices", description="A nice smell comes from there"),
        },
        world_id="outer"
    )

    oliver_place = World(
        id="oliver_place",
        name="The private oliver's world",
        description="Only Oliver comes here",
        initial_room_id="solitude",
        owner_user_id="oliver",
        visibility="public"
    )
    solitude = Room(
        id="solitude",
        name="Solitude",
        description="Where only one person fits",
        world_id="oliver_place"
    )

    easteregg_world = World(
        id="easteregg",
        name="Easter Egg",
        description="Only the best find this world",
        initial_room_id="easteregg_room",
        owner_user_id=None
    )
    easteregg_room = Room(
        id="easteregg_room",
        name="CONGRATS!",
        description="You found the easter egg :D",
        world_id="easteregg"
    )

    hunters_world = World(
        id="huntersworld",
        name="Hunters World",
        description="A nice place to practice targeting things",
        initial_room_id="honters",
        owner_user_id=None
    )
    hunters_room = Room(
        id="hunters",
        name="Shooting Range",
        description="A nice place to practice targeting things",
        world_id="huntersworld",
        items={
            "a cube": Item(name="a cube", description="a nice cube", visibility="auto"),
            "Not a cube": Item(name="Not a cube", description="a nice cube", visibility="auto"),
            "A sphere": Item(name="A sphere", description="a nice cube", visibility="auto"),
            "Not a sphere": Item(name="Not a sphere", description="a nice cube", visibility="auto"),
            "This is an awesome item yeah": Item(name="This is an awesome item yeah", description="a nice cube", visibility="auto"),
            "This is an awesome hidden item": Item(name="This is an awesome hidden item", description="a nice cube", visibility="hidden"),
        },
        exits={
            "Red laquered door": Exit(name="Red laquered door", description="a nice cube", visibility="hidden", destination_room_id="hunters"),
            "Blue laquered door": Exit(name="Blue laquered door", description="a nice cube", visibility="hidden", destination_room_id="hunters"),
            "This is an awesome exit": Exit(name="This is an awesome exit", description="Nice exit", visibility="listed", destination_room_id="hunters"),
        },
    )

    oliver = User(
        id="oliver",
        name="Oliver",
        email="oliver@example.com",
        world_id="outer",
        world_visit_record={
            "outer": WorldVisitRecord(
                world_id="outer",
                last_room_id="olivers"
            ),
            easteregg_world.id: WorldVisitRecord(
                world_id=easteregg_world.id,
                last_room_id="easteregg_room"
            )
        },
    )
    alice = User(
        id="alice",
        name="Alice",
        email="alice@example.com",
        world_id="outer",
        world_visit_record={
            "outer": WorldVisitRecord(
                world_id="outer",
                last_room_id="alices"
            ),
        },
    )
    bob = User(
        id="bob",
        name="Bob",
        email="bob@example.com",
        world_id="outer",
        world_visit_record={
            "outer": WorldVisitRecord(
                world_id="outer",
                last_room_id="bobs"
            ),
        },
        active=True,
    )
    charlie = User(
        id="charlie",
        name="Charlie",
        email="charlie@example.com",
        world_id=None,
        world_visit_record={
            "outer": WorldVisitRecord(
                world_id="outer",
                last_room_id="charlies"
            ),
        },
    )
    dave = User(
        id="dave",
        name="Dave",
        email="dave@example.com",
        world_id="outer",
        world_visit_record={
            "outer": WorldVisitRecord(
                world_id="outer",
                last_room_id="bobs"
            ),
        },
        active=True,
    )
    evan = User(
        id="evan",
        name="Evan",
        email="evan@example.com",
        world_id="outer",
        world_visit_record={
            "outer": WorldVisitRecord(
                world_id="outer",
                last_room_id="bobs"
            ),
        },
        active=False,
    )
    rabbit = User(
        id="rabbit",
        name="Rabbit",
        email="rabbit@example.com",
        world_id="rabbithole",
        world_visit_record={
            "rabbithole": WorldVisitRecord(
                world_id="rabbithole",
                last_room_id="rabbitholeroom"
            ),
            "outer": WorldVisitRecord(
                world_id="outer",
                last_room_id="bobs"
            ),
        },
    )
    hunter = User(
        id="hunter",
        name="Hunter",
        email="hunter@example.com",
        world_id="huntersworld",
        world_visit_record={
            "huntersworld": WorldVisitRecord(
                world_id="huntersworld",
                last_room_id="hunters"
            ),
        },
    )
    alice_completed_tutorial_mission = MissionLog(
        user_id="alice",
        mission_id="tutorial",
        completed_at=datetime.datetime.now(),
    )
    with uow as transaction:
        for mission in default_missions().all:
            transaction.missions.save_mission(mission)
        transaction.world_templates.save_world_template(emptytemplate)
        transaction.world_templates.save_world_template(monkstemplate)
        transaction.world_templates.save_world_template(templateforme)
        transaction.world_templates.save_world_template(braggingtemplate)
        transaction.world_templates.save_world_template(rabbittemplate)
        transaction.worlds.save_world(rabbithole_world)
        transaction.worlds.save_world(outer_world)
        transaction.worlds.save_world(public_tabern)
        transaction.worlds.save_world(oliver_place)
        transaction.worlds.save_world(easteregg_world)
        transaction.worlds.save_world(hunters_world)
        transaction.rooms.save_room(rabbithole_room)
        transaction.rooms.save_room(space)
        transaction.rooms.save_room(spaceship)
        transaction.rooms.save_room(olivers)
        transaction.rooms.save_room(private_bathroom)
        transaction.rooms.save_room(alices)
        transaction.rooms.save_room(bobs)
        transaction.rooms.save_room(a_table_in_the_tabern)
        transaction.rooms.save_room(solitude)
        transaction.rooms.save_room(easteregg_room)
        transaction.rooms.save_room(hunters_room)
        transaction.users.save_user(oliver)
        transaction.users.save_user(alice)
        transaction.users.save_user(bob)
        transaction.users.save_user(charlie)
        transaction.users.save_user(dave)
        transaction.users.save_user(evan)
        transaction.users.save_user(rabbit)
        transaction.users.save_user(hunter)
        transaction.missions.save_mission_log(alice_completed_tutorial_mission)

def createTestUow(db: bool = False) -> UnitOfWork:
    uow: UnitOfWork
    if db:
        uow = SQLAlchemyUnitOfWork(session_factory=db_connection())
    else:
        uow = FakeUnitOfWork()
    add_test_data(uow)
    return uow

def createTestArchitext(db: bool = False) -> Architext:
    uow = createTestUow(db)
    return Architext(uow,)


