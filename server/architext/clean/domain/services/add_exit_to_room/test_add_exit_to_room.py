import pytest
from architext.clean.domain.entities.room import Room
from architext.clean.domain.entities.exit import Exit
from architext.clean.domain.repositories.memory.room_repository import MemoryRoomRepository
from architext.clean.domain.services.add_exit_to_room.add_exit_to_room import add_exit_to_room


@pytest.fixture
def room_repository() -> MemoryRoomRepository:
    """Crea un repositorio de habitaciones en memoria limpio para cada prueba."""
    repo = MemoryRoomRepository()
    repo.save_room(Room(id="room1", name="Living Room", description="A cozy living room", exits=[]))
    repo.save_room(Room(id="room2", name="Kitchen", description="A modern kitchen", exits=[]))
    return repo


def test_add_exit_to_room_success(room_repository: MemoryRoomRepository):
    add_exit_to_room(
        room_repository=room_repository,
        id="room1",
        exit_name="To Kitchen",
        destination_room_id="room2"
    )

    room = room_repository.get_room_by_id("room1")
    assert len(room.exits) == 1
    assert room.exits[0].name == "To Kitchen"
    assert room.exits[0].destination_room_id == "room2"
    assert room.exits[0].description == ""
    assert room.exits[0].is_open is True
    assert room.exits[0].visibility == "listed"


def test_add_exit_to_room_invalid_room(room_repository: MemoryRoomRepository):
    with pytest.raises(KeyError):
        add_exit_to_room(
            room_repository=room_repository,
            id="room3",  
            exit_name="To Nowhere",
            destination_room_id="room2"
        )


@pytest.mark.skip(reason="to do")
def test_add_exit_to_room_empty_fields(room_repository: MemoryRoomRepository):
    with pytest.raises(ValueError):
        add_exit_to_room(
            room_repository=room_repository,
            id="room1",
            exit_name="",
            destination_room_id="room2"
        )

    with pytest.raises(ValueError):
        add_exit_to_room(
            room_repository=room_repository,
            id="room1",
            exit_name="To Kitchen",
            destination_room_id=""
        )


@pytest.mark.skip(reason="to do")
def test_add_exit_to_room_duplicate_exit_name(room_repository: MemoryRoomRepository):
    add_exit_to_room(
        room_repository=room_repository,
        id="room1",
        exit_name="To Kitchen",
        destination_room_id="room2"
    )

    with pytest.raises(ValueError):
        add_exit_to_room(
            room_repository=room_repository,
            id="room1",
            exit_name="To Kitchen",
            destination_room_id="room3"
        )
