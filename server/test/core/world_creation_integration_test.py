from typing import cast
from architext.chatbot.util import get_by_name
from architext.core.adapters.fake_external_event_publisher import FakeExternalEventPublisher
from architext.core.adapters.fake_uow import FakeUnitOfWork
from architext.core.commands import RequestWorldImport
import pytest # type: ignore
from architext.core.domain.entities.user import User
from architext.core.domain.events import WorldCreationRequested
from architext.core import Architext


ENCODED_TEMPLATE = """eJztVsFu2zAM/RXWl16CfsBu3i47bCiwBCuKIShkm6mJyaIhyVm9Iv8+yYkc27GddiiKHAoESSBSj4/iI6XniDU9khLyQYkCo08Q3VYWNdyRzEy0gKM9Q5NqKi2x8m7f0F4bwKdSskawOUKlaIva4JXfRoosuV2auXigzO8wpUjR2/yacSu/nqOBJXBYhoVB0HuuQLhwG8nCknoEUk3orTBWoTHAmx6VBQjJCm88FD6RPUQNYVbceDfhTU7lSMS7XFgQoChF8AgHFxdceJeT/ALMlgwlJMnW3iQqy9Fu7c/F4j739W4BvfzDzkAuhi/8t4blDLkY0hOX8TRvpT8QV7Afju8oUpOhKVBKB1qggY3mwh+PxpmcucE1Uxn7FDssYumCvD0J4WFfyuEzJ2/PIOHkpfGnpH3QYsoy239hUdrai/qc5F4tt07R2qY/o49VTgbcp+d3AyvH2K0KBbELCRmzBvebCJvrxiGWhl37mEL4A62SS2nFD2H24//0doknFRylkojsvydFF7hPqlKSjMWsT2xUV+/I6vSolphqtF0Fdnl8r8HsHUwqSoSSs9f3b05ZhmrQwZ0zaTppJPihOYL1XCZxpy+n0fo+5zHLWouCsmnAjsN42gOOZaeGY/xaex9tVE1ORZrnyB3tU+ocmaRd+bQd7aZZOy29EUpNW2FxTsVf+Q/IKv1d+6lK1snXjbw9CuTCDdp2s3/5+Jns/19d3L0/efUcJ2JbkvnRGy6eodvFXSGX8cJ690tkstJhUyA3yyxUue/0UePLeawM6rze/QOfZbhJ"""


def test_world_import_integration_success(architext: Architext):
    out = architext.handle(RequestWorldImport(
        name="new world",
        description="nice",
        text_representation=ENCODED_TEMPLATE,
        format='encoded'
    ), client_user_id="oliver")

    with architext._uow as transaction:
        external_events = cast(FakeExternalEventPublisher, transaction.external_events)
        creation_request_event = next((event for event in external_events.published_events if type(event) == WorldCreationRequested), None)
        assert creation_request_event is not None
        assert creation_request_event.format == 'encoded'
        assert creation_request_event.user_id == "oliver"
        assert creation_request_event.text_representation == ENCODED_TEMPLATE
        new_world = get_by_name("new world", transaction.worlds.list_worlds())
        assert len(transaction.rooms.list_rooms_by_world(new_world.id)) == 6
