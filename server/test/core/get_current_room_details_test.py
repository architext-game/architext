from architext.chatbot.util import get_by_name
from architext.core.queries.get_room_details import GetRoomDetails
import pytest # type: ignore
from architext.core import Architext


def test_get_room_success(architext: Architext):
    result = architext.query(GetRoomDetails(), client_user_id="oliver")

    assert result.room is not None
    assert result.room.name == "Oliver's Room"
    assert "This is Oliver's Room" in result.room.description


def test_get_room_details_returns_users_in_room(architext: Architext):
    result = architext.query(GetRoomDetails(room_id="bobs"), client_user_id="oliver")

    assert result.room is not None
    assert len(result.room.people) == 3
    assert get_by_name("Bob", result.room.people).active == True
    assert get_by_name("Dave", result.room.people).active == True
    assert get_by_name("Evan", result.room.people).active == False


def test_get_room_user_not_in_room(architext: Architext):
    with pytest.raises(PermissionError):
        result = architext.query(GetRoomDetails(), client_user_id="charlie")

def test_get_room_invalid_user_id(architext: Architext):
    with pytest.raises(Exception, match="You need to be authenticated"):
        result = architext.query(GetRoomDetails(), client_user_id="invalid")

def test_underprivileged_user_cannot_get_details(architext: Architext):
    with pytest.raises(PermissionError):
        result = architext.query(GetRoomDetails(), client_user_id="alice")

def test_hidden_exit_does_appear(architext: Architext):
    result = architext.query(GetRoomDetails(), client_user_id="oliver")
    assert result.room is not None
    assert next((exit for exit in result.room.exits if exit.name == "Secret exit"), None) is not None
