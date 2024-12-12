import pytest
from architext.adapters.memory_uow import MemoryUnitOfWork
from architext.core.services.create_connected_room import create_connected_room, CreateConnectedRoomInput

from architext.core.domain.entities.room import Room
from architext.core.domain.entities.user import User


@pytest.fixture
def uow() -> MemoryUnitOfWork:
    uow = MemoryUnitOfWork()
    uow.rooms.save_room(Room(id="kitchen", name="The Kitchen", description="A beautiful kitchen.", exits=[]))
    uow.users.save_user(User(name="Oliver", email="asds@asdsa.com", id="0", room_id="kitchen", password_hash=b"adasd"))
    return uow


def test_create_connected_room_success(uow: MemoryUnitOfWork):
    out = create_connected_room(
        uow=uow,
        input=CreateConnectedRoomInput(
            name="Living Room",
            description="A cozy living room",
            exit_to_new_room_name="Door to living room",
            exit_to_new_room_description="A door leading to the living room",
            exit_to_old_room_name="Door to kitchen",
            exit_to_old_room_description="A door leading to the kitchen"
        ),
        client_user_id="0"
    )

    new_room = uow.rooms.get_room_by_id(out.id)
    old_room = uow.rooms.get_room_by_id("kitchen")
    assert uow.committed
    assert new_room is not None
    assert old_room is not None
    assert new_room.name == "Living Room"
    assert new_room.description == "A cozy living room"
    assert next(exit for exit in new_room.exits if exit.name == "Door to kitchen").description == "A door leading to the kitchen"
    assert next(exit for exit in old_room.exits if exit.name == "Door to living room").description == "A door leading to the living room"


@pytest.mark.skip(reason="to do")
def test_create_room_duplicate_exit_name_fails(uow: MemoryUnitOfWork):
    assert False

