from typing import cast
from architext.core.adapters.fake.external_event_publisher import FakeExternalEventPublisher
from architext.core.adapters.fake.uow import FakeUnitOfWork
from architext.core.commands import RequestWorldCreationFromTemplate
from architext.core.domain.entities.world_template import WorldTemplate
import pytest # type: ignore
from architext.core.domain.entities.user import User
from architext.core.domain.events import WorldCreationRequested
from architext.core import Architext


def test_requests_world_creation(architext: Architext):
    architext.handle(RequestWorldCreationFromTemplate(
        name="new world",
        description="nice",
        template_id="monksriddletemplate"
    ), client_user_id="oliver")

    with architext._uow as transaction:
        external_events = cast(FakeExternalEventPublisher, transaction.external_events)
        external_events.published_events
        creation_request_event = next((event for event in external_events.published_events if type(event) == WorldCreationRequested), None)
        assert creation_request_event is not None
        assert creation_request_event.format == 'encoded'
        assert creation_request_event.user_id == "oliver"
        template = transaction.world_templates.get_world_template_by_id("monksriddletemplate")
        assert template is not None
        assert creation_request_event.text_representation == template.world_encoded_json


def test_world_is_created(architext: Architext):
    out = architext.handle(RequestWorldCreationFromTemplate(
        name="new world",
        description="nice",
        template_id="monksriddletemplate",
    ), client_user_id="oliver")

    with architext._uow as transaction:
        world = transaction.worlds.get_world_by_id(out.future_world_id)
        assert world is not None
        assert world.name == "new world"
        assert world.description == "nice"
        assert world.base_template_id == "monksriddletemplate"
        assert len(transaction.rooms.list_rooms()) == 46
