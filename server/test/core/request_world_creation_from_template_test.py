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
        world_encoded_json="""eJztVsFu2zAM/RXWl16CfsBu3i47bCiwBCuKIShkm6mJyaIhyVm9Iv8+yYkc27GddiiKHAoESSBSj4/iI6XniDU9khLyQYkCo08Q3VYWNdyRzEy0gKM9Q5NqKi2x8m7f0F4bwKdSskawOUKlaIva4JXfRoosuV2auXigzO8wpUjR2/yacSu/nqOBJXBYhoVB0HuuQLhwG8nCknoEUk3orTBWoTHAmx6VBQjJCm88FD6RPUQNYVbceDfhTU7lSMS7XFgQoChF8AgHFxdceJeT/ALMlgwlJMnW3iQqy9Fu7c/F4j739W4BvfzDzkAuhi/8t4blDLkY0hOX8TRvpT8QV7Afju8oUpOhKVBKB1qggY3mwh+PxpmcucE1Uxn7FDssYumCvD0J4WFfyuEzJ2/PIOHkpfGnpH3QYsoy239hUdrai/qc5F4tt07R2qY/o49VTgbcp+d3AyvH2K0KBbELCRmzBvebCJvrxiGWhl37mEL4A62SS2nFD2H24//0doknFRylkojsvydFF7hPqlKSjMWsT2xUV+/I6vSolphqtF0Fdnl8r8HsHUwqSoSSs9f3b05ZhmrQwZ0zaTppJPihOYL1XCZxpy+n0fo+5zHLWouCsmnAjsN42gOOZaeGY/xaex9tVE1ORZrnyB3tU+ocmaRd+bQd7aZZOy29EUpNW2FxTsVf+Q/IKv1d+6lK1snXjbw9CuTCDdp2s3/5+Jns/19d3L0/efUcJ2JbkvnRGy6eodvFXSGX8cJ690tkstJhUyA3yyxUue/0UePLeawM6rze/QOfZbhJ"""
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
    assert len(fake_uow.rooms.list_rooms()) == 6
