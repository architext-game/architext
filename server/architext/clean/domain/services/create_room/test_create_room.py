import pytest
from architext.clean.domain.repositories.memory.room_repository import MemoryRoomRepository
from architext.clean.domain.services.create_room.create_room import create_room


@pytest.fixture
def room_repository() -> MemoryRoomRepository:
    return MemoryRoomRepository()


def test_create_room_success(room_repository: MemoryRoomRepository):
    room_id = create_room(
        room_repository=room_repository,
        name="Living Room",
        id="room1",
        description="A cozy living room"
    )

    saved_room = room_repository.get_room_by_id("room1")
    assert saved_room.id == "room1"
    assert saved_room.name == "Living Room"
    assert saved_room.description == "A cozy living room"
    assert room_id == "room1"

@pytest.mark.skip(reason="to do")
def test_create_room_duplicate_id(room_repository: MemoryRoomRepository):
    create_room(
        room_repository=room_repository,
        name="Living Room",
        id="room1",
        description="A cozy living room"
    )

    with pytest.raises(KeyError):
        create_room(
            room_repository=room_repository,
            name="Kitchen",
            id="room1",  # Mismo ID
            description="A modern kitchen"
        )

@pytest.mark.skip(reason="to do")
def test_create_room_empty_fields(room_repository: MemoryRoomRepository):
    with pytest.raises(ValueError):
        create_room(
            room_repository=room_repository,
            name="",
            id="room1",
            description="Description without a name"
        )

    with pytest.raises(ValueError):
        create_room(
            room_repository=room_repository,
            name="Living Room",
            id="",
            description="Description without an ID"
        )

    with pytest.raises(ValueError):
        create_room(
            room_repository=room_repository,
            name="Living Room",
            id="room1",
            description=""
        )


def test_create_room_list_rooms(room_repository: MemoryRoomRepository):
    create_room(
        room_repository=room_repository,
        name="Living Room",
        id="room1",
        description="A cozy living room"
    )
    create_room(
        room_repository=room_repository,
        name="Kitchen",
        id="room2",
        description="A modern kitchen"
    )

    rooms = room_repository.list_rooms()
    assert len(rooms) == 2
    assert rooms[0].id == "room1"
    assert rooms[1].id == "room2"
