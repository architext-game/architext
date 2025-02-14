from typing import cast
from architext.core.adapters.fake_uow import FakeUnitOfWork
from architext.core.domain.entities.world import DEFAULT_WORLD
from architext.core.messagebus import MessageBus
from architext.core.queries.get_current_room import GetCurrentRoom, GetCurrentRoomResult
import pytest # type: ignore
from architext.core.domain.entities.user import User
from architext.core.domain.entities.room import Room
from architext.core import Architext
from test.fixtures import createTestArchitext


@pytest.fixture
def architext() -> Architext:
    return createTestArchitext()


def test_get_current_room_success(architext: Architext):
    result = architext.query(GetCurrentRoom(), client_user_id="oliver")

    assert result.current_room is not None
    assert result.current_room.name == "Oliver's Room"
    assert "This is Oliver's Room" in result.current_room.description


def test_get_current_room_user_not_in_room(architext: Architext):
    result = architext.query(GetCurrentRoom(), client_user_id="charlie")
    assert result.current_room is None


def test_get_current_room_invalid_user_id(architext: Architext):
    with pytest.raises(Exception, match="You need to be authenticated"):
        result = architext.query(GetCurrentRoom(), client_user_id="invalid")


def test_get_current_room_lists_people_in_room(architext: Architext):
    result = architext.query(GetCurrentRoom(), client_user_id="dave")
    assert result.current_room is not None
    assert len(result.current_room.people) == 2  # two ACTIVE players
    assert "Bob" in [person.name for person in result.current_room.people]


def test_get_current_room_lists_items_in_room(architext: Architext):
    result = architext.query(GetCurrentRoom(), client_user_id="oliver")
    assert result.current_room is not None
    assert len(result.current_room.items) == 4
    items = {item.name: item for item in result.current_room.items}
    assert "A cube" in items
    assert "A small cube" in items
    assert "A toroid" in items
    assert "A sphere" in items
    assert "A pyramid" not in items  # hidden item
    assert items["A cube"].list_in_room_description  # not mentioned auto
    assert not items["A small cube"].list_in_room_description  # mentioned auto
    assert not items["A toroid"].list_in_room_description  # unlisted
    assert items["A sphere"].list_in_room_description  # listed


def test_hidden_exit_does_not_appear(architext: Architext):
    result = architext.query(GetCurrentRoom(), client_user_id="oliver")
    assert result.current_room is not None
    assert next((exit for exit in result.current_room.exits if exit.name == "Secret exit"), None) is None

    # It's easy for this test to give a false positive 
    # if the secret exit is removed from the fixtures,
    # so let'd check that it's still there
    uow = cast(FakeUnitOfWork, architext._uow)
    room = uow.rooms.get_room_by_id("olivers")
    assert room is not None
    exit = room.exits.get("Secret exit")
    assert exit is not None
    
