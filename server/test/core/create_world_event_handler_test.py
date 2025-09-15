from typing import cast
from architext.chatbot.util import get_by_name
from architext.core.adapters.fake.external_event_publisher import FakeExternalEventPublisher
from architext.core.adapters.fake.uow import FakeUnitOfWork
from architext.core.domain.events import WorldCreated, WorldCreationRequested
from architext.core import Architext
from architext.core.handlers.import_world import import_world
import uuid
from architext.content.the_monks_riddle import THE_MONKS_RIDDLE

ENCODED_TEMPLATE = """eJx9kcFOwzAMhl/F9MKl4gG4TRxB4jCkCaFpilp3tZbEVZxOG9Penbi0tIPSS6LE9v/5ty8ZB9qTN3bnjcPsEbLXNmKADdlSshzGeIlSBGoisde0F4z3AnhqLAeEWCO0no4YBO+0jDxFSlWB2e2o1ApWYX1rXG9Jvx+XbCY69LJuTIH68Qv+zi2YhK0sm0h+D+S7Fo5GokcR4OqmpRyMZY8PKoUnij15wLxxly1Kk5qaGeKmNhEMeCoQVKFPSXCjKVOfo8x1e81hMHijPpBX8MSfZ1gvkFdQ/EmZ9/BMsajRz2p0jYtDa5OcQ4EqsFPXAResHHrFzsaE9N9e+kEWbMvvA10Tz7qRBci4+Zt5HUY3A3nJoOMSg4dJ1c+Qtkn3C67G+X8="""

def test_import_the_monks_riddle(architext: Architext):
    world_id = str(uuid.uuid4())

    import_world(architext._uow, WorldCreationRequested(
        text_representation=THE_MONKS_RIDDLE,
        format='plain',
        user_id="oliver",
        world_name="The Monk's Riddleasdf",
        world_description="A monastery full of mistery.",
        future_world_id=world_id,
        visibility='private',
    ))
    with architext._uow as transaction:
        world = get_by_name("The Monk's Riddleasdf", transaction.worlds.list_worlds())
        assert world.name == "The Monk's Riddleasdf"
        assert len(transaction.rooms.list_rooms_by_world(world.id)) == 35
        initial_room = transaction.rooms.get_room_by_id(world.initial_room_id)
        assert initial_room is not None
        assert "a poster" in initial_room.items
        assert "a traslucent portal" in initial_room.exits


def test_world_created_event_is_published(architext: Architext):
    world_id = str(uuid.uuid4())

    import_world(architext._uow, WorldCreationRequested(
        text_representation=THE_MONKS_RIDDLE,
        format='plain',
        user_id="oliver",
        world_name="The Monk's Riddle",
        world_description="A monastery full of mistery.",
        future_world_id=world_id,
        visibility='private',
    ))
    uow = cast(FakeUnitOfWork, architext._uow)
    with uow as transaction:
        external_events = cast(FakeExternalEventPublisher, transaction.external_events)
        world_created_event = next((event for event in external_events.published_events if type(event) == WorldCreated), None)
        assert world_created_event is not None
        assert world_created_event.owner_id == "oliver"
        world_id = world_created_event.world_id
        world = transaction.worlds.get_world_by_id(world_id)
        assert world is not None
        assert world.name == "The Monk's Riddle"
