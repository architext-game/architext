from architext.core.queries.get_room_details import GetRoomDetails
import pytest # type: ignore
from architext.core import Architext
from architext.core.queries.get_thing_in_room import GetThingInRoom


def test_get_item_in_room(architext: Architext):
    result = architext.query(GetThingInRoom(partial_name="toroid"), client_user_id="oliver")

    assert result.status == "item_matched"
    assert result.item_match is not None
    assert result.item_match.name == "A toroid"
    assert result.item_match.description == "a nice toroid"


def test_get_hidden_item_in_room(architext: Architext):
    result = architext.query(GetThingInRoom(partial_name="hidden"), client_user_id="oliver")

    assert result.status == "item_matched"
    assert result.item_match is not None
    assert result.item_match.name == "The hidden"
    assert result.item_match.description == "a nice pyramid"


def test_get_hidden_item_with_uncomplete_word_finds_none(architext: Architext):
    result = architext.query(GetThingInRoom(partial_name="pyra"), client_user_id="oliver")

    assert result.status == "none_found"
    assert result.item_match is None
    assert result.exit_match is None


def test_get_hidden_item_with_match_less_than_35_percent_finds_none(architext: Architext):
    result = architext.query(GetThingInRoom(partial_name="One"), client_user_id="oliver")
 
    assert result.status == "none_found"
    assert result.item_match is None
    assert result.exit_match is None


def test_get_exit_in_room(architext: Architext):
    result = architext.query(GetThingInRoom(partial_name="alice"), client_user_id="oliver")
 
    assert result.status == "exit_matched"
    assert result.exit_match is not None
    assert result.exit_match.name == "To Alice's Room"
    assert result.exit_match.description == "A nice smell comes from there"


def test_get_hidden_exit_in_room(architext: Architext):
    result = architext.query(GetThingInRoom(partial_name="Secret exit"), client_user_id="oliver")
 
    assert result.status == "exit_matched"
    assert result.exit_match is not None
    assert result.exit_match.name == "Secret exit"
    assert result.exit_match.description == "My secret scape pod"
    

def test_get_thing_ambiguous_name_among_non_hidden_things(architext: Architext):
    result = architext.query(GetThingInRoom(partial_name="a"), client_user_id="oliver")
 
    assert result.status == "multiple_matches"
    assert result.exit_match is None
    assert result.item_match is None
    assert "A cube" in result.multiple_matches
    assert "A small cube" in result.multiple_matches
    assert "A sphere" in result.multiple_matches
    assert "A toroid" in result.multiple_matches
    assert "A pyramid" not in result.multiple_matches  # it is hidden


def test_get_thing_exact_name_that_is_substring_of_another_things_name(architext: Architext):
    # Case where case matches between the two things.
    # There is "a cube" and "Not a cube" in the room.
    result = architext.query(GetThingInRoom(partial_name="a cube"), client_user_id="hunter")
 
    assert result.status == "item_matched"
    assert result.item_match is not None
    assert result.item_match.name == "a cube"

    # Case where case doesn't match between the two things,
    # nor between the input and the target.
    # There is "A sphere" and "Not a sphere" in the room.
    result = architext.query(GetThingInRoom(partial_name="a sphere"), client_user_id="hunter")
 
    assert result.status == "item_matched"
    assert result.item_match is not None
    assert result.item_match.name == "A sphere"


def test_get_thing_ambiguous_name_among_hidden_things_finds_none(architext: Architext):
    result = architext.query(GetThingInRoom(partial_name="laquered door"), client_user_id="hunter")
 
    assert result.status == "none_found"
    assert result.item_match is None
    assert result.exit_match is None
    assert len(result.multiple_matches) == 0    


def test_get_thing_ambiguous_name_among_hidden_and_non_hidden_things_ignores_hidden(architext: Architext):
    result = architext.query(GetThingInRoom(partial_name="This is an awesome"), client_user_id="hunter")
 
    assert result.status == "multiple_matches"
    assert result.exit_match is None
    assert result.item_match is None
    assert "This is an awesome item yeah" in result.multiple_matches
    assert "This is an awesome exit" in result.multiple_matches
    assert "This is an awesome item hidden" not in result.multiple_matches
    assert len(result.multiple_matches) == 2

    result = architext.query(GetThingInRoom(partial_name="This is an awesome item"), client_user_id="hunter")
 
    assert result.status == "item_matched"
    assert result.item_match is not None
    assert result.item_match.name == "This is an awesome item yeah"


def test_get_thing_by_user_that_is_not_in_a_room_fails(architext: Architext):
    with pytest.raises(PermissionError):
        architext.query(GetRoomDetails(), client_user_id="charlie")


def test_get_thing_by_invalid_user_id(architext: Architext):
    with pytest.raises(Exception, match="You need to be authenticated"):
        architext.query(GetRoomDetails(), client_user_id="invalid")

