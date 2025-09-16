from architext.core.application.commands import EnterWorld
from architext.core import Architext
import pytest # type: ignore


def test_enter_world_for_the_first_time_puts_user_in_starting_room(architext: Architext):
    architext.handle(EnterWorld(world_id="outer"), client_user_id="hunter")

    with architext._uow as transaction:
        hunter = transaction.users.get_user_by_id("hunter")
        assert hunter is not None
        assert hunter.room_id == "space"
        room = transaction.rooms.get_room_by_id(hunter.room_id)
        assert room is not None
        assert room.world_id == "outer"
        world = transaction.worlds.get_world_by_id(room.world_id)
        assert world is not None
        assert world.name == "Outer Wilds"


def test_enter_world_again_puts_user_in_last_visited_room(architext: Architext):
    architext.handle(EnterWorld(world_id="outer"), client_user_id="rabbit")

    with architext._uow as transaction:
        rabbit = transaction.users.get_user_by_id("rabbit")
        assert rabbit is not None
        assert rabbit.room_id == "bobs"
        room = transaction.rooms.get_room_by_id(rabbit.room_id)
        assert room is not None
        assert room.world_id == "outer"
        world = transaction.worlds.get_world_by_id(room.world_id)
        assert world is not None
        assert world.name == "Outer Wilds"


def test_enter_world_that_does_not_exist(architext: Architext):
    with pytest.raises(ValueError, match="World does not exist."):
        architext.handle(EnterWorld(world_id="aasdasdasdas"), client_user_id="rabbit")


@pytest.mark.skip(reason="TODO")
def test_user_changed_room_event_gets_invoked() -> None:
    pass

@pytest.mark.skip(reason="TODO")
def test_users_get_notified_if_user_enters_world_in_its_room() -> None:
    pass

@pytest.mark.skip(reason="TODO")
def test_users_get_notified_if_user_leaves_world_from_its_room() -> None:
    pass
