from typing import cast
from architext.core.adapters.fake_external_event_publisher import FakeExternalEventPublisher
from architext.core.adapters.fake_uow import FakeUnitOfWork
from architext.core.domain.entities.user import User
from architext.core.domain.events import WorldCreated, WorldCreationRequested
import pytest # type: ignore
from architext.core import Architext
from architext.core.handlers.import_world import import_world

ENCODED_TEMPLATE = """eJx9kcFOwzAMhl/F9MKl4gG4TRxB4jCkCaFpilp3tZbEVZxOG9Penbi0tIPSS6LE9v/5ty8ZB9qTN3bnjcPsEbLXNmKADdlSshzGeIlSBGoisde0F4z3AnhqLAeEWCO0no4YBO+0jDxFSlWB2e2o1ApWYX1rXG9Jvx+XbCY69LJuTIH68Qv+zi2YhK0sm0h+D+S7Fo5GokcR4OqmpRyMZY8PKoUnij15wLxxly1Kk5qaGeKmNhEMeCoQVKFPSXCjKVOfo8x1e81hMHijPpBX8MSfZ1gvkFdQ/EmZ9/BMsajRz2p0jYtDa5OcQ4EqsFPXAResHHrFzsaE9N9e+kEWbMvvA10Tz7qRBci4+Zt5HUY3A3nJoOMSg4dJ1c+Qtkn3C67G+X8="""

@pytest.fixture
def architext() -> Architext:
    uow = FakeUnitOfWork()
    oliver = User(
        id="oliver",
        name="Oliver",
        email="oliver@example.com",
        room_id="rabbithole",
        password_hash=b"asdasd"
    )
    uow.users.save_user(oliver)
    return Architext(uow)


def test_world_creation_requested_event_handler(architext: Architext):
    out = import_world(architext._uow, WorldCreationRequested(
        text_representation=ENCODED_TEMPLATE,
        format='encoded',
        user_id="oliver",
        world_description="Nice world",
        world_name="new world"
    ))
    world = architext._uow.worlds.list_worlds()[0]
    assert world.name == "new world"
    world_id = world.id
    assert len(architext._uow.rooms.list_rooms_by_world(world_id)) == 3


def test_world_created_event_is_published(architext: Architext):
    out = import_world(architext._uow, WorldCreationRequested(
        text_representation=ENCODED_TEMPLATE,
        format='encoded',
        user_id="oliver",
        world_description="Nice world",
        world_name="new world"
    ))

    uow = cast(FakeUnitOfWork, architext._uow)
    external_events = cast(FakeExternalEventPublisher, architext._uow.external_events)
    world_created_event = next((event for event in external_events.published_events if type(event) == WorldCreated), None)
    assert world_created_event is not None
    assert world_created_event.owner_id == "oliver"
    world_id = world_created_event.world_id
    world = uow.worlds.get_world_by_id(world_id)
    assert world is not None
    assert world.name == "new world"
    assert world.owner_user_id == "oliver"
    rooms = uow.rooms.list_rooms_by_world(world_id)
    assert len(rooms) == 3
