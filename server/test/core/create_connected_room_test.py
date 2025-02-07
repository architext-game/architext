from typing import cast
from architext.core.facade import Architext
import pytest # type: ignore
from architext.core.adapters.fake_uow import FakeUnitOfWork
from architext.core.messagebus import MessageBus
from architext.core.services.create_connected_room import CreateConnectedRoom, CreateConnectedRoomResult
from architext.core.services.create_initial_data import CreateInitialData
from architext.core.commands import CreateConnectedRoom

from architext.core.domain.entities.room import Room
from architext.core.domain.entities.user import User
from architext.core.domain.entities.world import DEFAULT_WORLD, World

from test.fixtures import createTestArchitext

@pytest.fixture
def architext() -> Architext:
    return createTestArchitext()

def test_create_connected_room_success(architext: Architext):
    command = CreateConnectedRoom(
        name="Living Room",
        description="A cozy living room",
        exit_to_new_room_name="Door to living room",
        exit_to_new_room_description="A door leading to the living room",
        exit_to_old_room_name="Door to kitchen",
        exit_to_old_room_description="A door leading to the kitchen"
    )
    out: CreateConnectedRoomResult = architext.handle(command, client_user_id="oliver")

    uow = cast(FakeUnitOfWork, architext._uow)
    new_room = uow.rooms.get_room_by_id(out.room_id)
    old_room = uow.rooms.get_room_by_id("olivers")
    assert uow.committed
    assert new_room is not None
    assert old_room is not None
    assert new_room.name == "Living Room"
    assert new_room.description == "A cozy living room"
    assert new_room.exits["Door to kitchen"].description == "A door leading to the kitchen"
    assert old_room.exits["Door to living room"].description == "A door leading to the living room"


def test_unauthorized_user_fails(architext: Architext):
    command = CreateConnectedRoom(
        name="Living Room",
        description="A cozy living room",
        exit_to_new_room_name="Door to living room",
        exit_to_new_room_description="A door leading to the living room",
        exit_to_old_room_name="Door to kitchen",
        exit_to_old_room_description="A door leading to the kitchen"
    )
    with pytest.raises(PermissionError):
        architext.handle(command, client_user_id="alice")


@pytest.mark.skip(reason="to do")
def test_create_room_duplicate_exit_name_fails(uow: FakeUnitOfWork):
    assert False

