from typing import cast
import pytest # type: ignore
from architext.core.adapters.fake_uow import FakeUnitOfWork
from architext.core.commands import DeleteRoom
from architext.core import Architext
from architext.core.adapters.fake_uow import FakeUnitOfWork
from test.fixtures import createTestData


@pytest.fixture
def architext() -> Architext:
    return createTestData()


def test_delete_room_deletes_room(architext: Architext) -> None:
    command = DeleteRoom()
    architext.handle(command, "oliver")

    uow = cast(FakeUnitOfWork, architext._uow)
    room = uow.rooms.get_room_by_id("olivers")
    assert room is None


def test_delete_room_deletes_connected_exits(architext: Architext) -> None:
    command = DeleteRoom()
    architext.handle(command, "oliver")

    uow = cast(FakeUnitOfWork, architext._uow)
    rooms = uow.rooms.list_rooms()
    for room in rooms:
        assert next((exit for exit in room.exits.values() if exit.destination_room_id == "olivers"), None) is None


def test_delete_room_moves_users_to_initial_room(architext: Architext) -> None:
    command = DeleteRoom()
    architext.handle(command, "oliver")
    uow = cast(FakeUnitOfWork, architext._uow)

    user = uow.users.get_user_by_id("oliver")
    assert user is not None
    assert user.room_id == "space"


def test_delete_rooms_initial_room_fails(architext: Architext):
    with pytest.raises(ValueError, match="The initial room of a world can't be deleted."):
        architext.handle(DeleteRoom(), "rabbit")


def test_delete_room_without_privileges_fails(architext: Architext):
    with pytest.raises(PermissionError, match="You need to be the owner of the world to do that"):
        architext.handle(DeleteRoom(), "alice")
