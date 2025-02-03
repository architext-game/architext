from typing import cast
from architext.core.adapters.fake_uow import FakeUnitOfWork
from architext.core.domain.entities.world import DEFAULT_WORLD
from architext.core.messagebus import MessageBus
from architext.core.services.get_current_room import get_current_room
from architext.core.commands import GetCurrentRoom, GetCurrentRoomResult
import pytest # type: ignore
from architext.core.domain.entities.user import User
from architext.core.domain.entities.room import Room
from architext.core import Architext
from test.fixtures import createTestData


@pytest.fixture
def architext() -> Architext:
    return createTestData()


def test_get_current_room_success(architext: Architext):
    result: GetCurrentRoomResult = architext.handle(GetCurrentRoom(), client_user_id="oliver")

    assert result.current_room is not None
    assert result.current_room.id == "olivers"
    assert result.current_room.name == "Oliver's Room"
    assert result.current_room.description == "This is Oliver's Room"


def test_get_current_room_user_not_in_room(architext: Architext):
    result: GetCurrentRoomResult = architext.handle(GetCurrentRoom(), client_user_id="charlie")
    assert result.current_room is None


def test_get_current_room_invalid_user_id(architext: Architext):
    with pytest.raises(ValueError):
        result: GetCurrentRoomResult = architext.handle(GetCurrentRoom(), client_user_id="invalid")


def test_get_current_room_lists_people_in_room(architext: Architext):
    result: GetCurrentRoomResult = architext.handle(GetCurrentRoom(), client_user_id="dave")
    assert result.current_room is not None
    assert len(result.current_room.people) == 2
    assert "Bob" in [person.name for person in result.current_room.people]


def test_hidden_exit_does_not_appear(architext: Architext):
    result: GetCurrentRoomResult = architext.handle(GetCurrentRoom(), client_user_id="oliver")
    assert result.current_room is not None
    assert next((exit for exit in result.current_room.exits if exit.name == "Secret exit"), None) is None

    # It's easy for this test to give a false positive 
    # if the secret exit is removed from the fixtures,
    # so let'd check that it's still there
    uow = cast(FakeUnitOfWork, architext._uow)
    room = uow.rooms.get_room_by_id("olivers")
    assert room is not None
    exit = next((exit for exit in room.exits if exit.name == "Secret exit"), None)
    assert exit is not None
    
