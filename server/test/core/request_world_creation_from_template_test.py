from typing import cast
from architext.core.adapters.fake_external_event_publisher import FakeExternalEventPublisher
from architext.core.adapters.fake_uow import FakeUnitOfWork
from architext.core.commands import RequestWorldCreationFromTemplate
from architext.core.domain.entities.world_template import WorldTemplate
import pytest # type: ignore
from architext.core.domain.entities.user import User
from architext.core.domain.events import WorldCreationRequested
from architext.core import Architext


@pytest.fixture
def architext() -> Architext:
    uow = FakeUnitOfWork()
    oliver = User(
        id="oliver",
        name="Oliver",
        email="oliver@example.com",
        room_id=None,
        password_hash=b"asdasd"
    )
    template = WorldTemplate(
        author_id="oliver",
        description="A nice template",
        name="my first template",
        id="template01",
        world_encoded_json="""eJx9kcFOwzAMhl/F9MKl4gG4TRxB4jCkCaFpilp3tZbEVZxOG9Penbi0tIPSS6LE9v/5ty8ZB9qTN3bnjcPsEbLXNmKADdlSshzGeIlSBGoisde0F4z3AnhqLAeEWCO0no4YBO+0jDxFSlWB2e2o1ApWYX1rXG9Jvx+XbCY69LJuTIH68Qv+zi2YhK0sm0h+D+S7Fo5GokcR4OqmpRyMZY8PKoUnij15wLxxly1Kk5qaGeKmNhEMeCoQVKFPSXCjKVOfo8x1e81hMHijPpBX8MSfZ1gvkFdQ/EmZ9/BMsajRz2p0jYtDa5OcQ4EqsFPXAResHHrFzsaE9N9e+kEWbMvvA10Tz7qRBci4+Zt5HUY3A3nJoOMSg4dJ1c+Qtkn3C67G+X8="""
    )
    with uow:
        uow.users.save_user(oliver)
        uow.world_templates.save_world_template(template)
        uow.commit()
    return Architext(uow)


def test_requests_world_creation(architext: Architext):
    out = architext.handle(RequestWorldCreationFromTemplate(
        name="new world",
        description="nice",
        template_id="template01"
    ), client_user_id="oliver")

    fake_uow = cast(FakeUnitOfWork, architext._uow)
    external_events = cast(FakeExternalEventPublisher, architext._uow.external_events)
    external_events.published_events
    creation_request_event = next((event for event in external_events.published_events if type(event) == WorldCreationRequested), None)
    assert creation_request_event is not None
    assert creation_request_event.format == 'encoded'
    assert creation_request_event.user_id == "oliver"
    template = fake_uow.world_templates.get_world_template_by_id("template01")
    assert template is not None
    assert creation_request_event.text_representation == template.world_encoded_json


def test_world_is_created(architext: Architext):
    out = architext.handle(RequestWorldCreationFromTemplate(
        name="new world",
        description="nice",
        template_id="template01",
    ), client_user_id="oliver")

    fake_uow = cast(FakeUnitOfWork, architext._uow)
    world = fake_uow.worlds.get_world_by_id(out.future_world_id)
    assert world is not None
    assert world.name == "new world"
    assert world.description == "nice"
    assert world.base_template_id == "template01"
    assert len(fake_uow.rooms.list_rooms()) == 3
