import pytest
from architext.clean.domain.entities.user import User
from architext.clean.domain.entities.room import Room
from architext.clean.domain.entities.exit import Exit
from architext.clean.domain.repositories.memory.room_repository import MemoryRoomRepository
from architext.clean.domain.services.traverse_exit.traverse_exit import traverse_exit


@pytest.fixture
def room_repository() -> MemoryRoomRepository:
    """Crea un repositorio de habitaciones en memoria con habitaciones y salidas."""
    repo = MemoryRoomRepository()
    room1 = Room(
        id="room1",
        name="Living Room",
        description="A cozy living room",
        exits=[
            Exit(name="To Kitchen", destination_room_id="room2", description="", is_open=True, key_names=[], visibility="listed")
        ]
    )
    room2 = Room(
        id="room2",
        name="Kitchen",
        description="A modern kitchen",
        exits=[]
    )
    repo.save_room(room1)
    repo.save_room(room2)
    return repo


@pytest.fixture
def user_in_room() -> User:
    """Crea un usuario que está en una habitación."""
    return User(name="John", email="john@example.com", room_id="room1", password_hash=b"asdasd")


@pytest.fixture
def user_not_in_room() -> User:
    """Crea un usuario que no está en ninguna habitación."""
    return User(name="Alice", email="alice@example.com", room_id=None, password_hash=b"asdasd")


def test_traverse_exit_success(room_repository: MemoryRoomRepository, user_in_room: User):
    """Test para verificar que un usuario puede atravesar una salida exitosamente."""
    new_room_id = traverse_exit(room_repository, user_in_room, exit_name="To Kitchen")

    assert new_room_id == "room2"
    assert user_in_room.room_id == "room2"


def test_traverse_exit_user_not_in_room(room_repository: MemoryRoomRepository, user_not_in_room: User):
    """Test para verificar que se lanza un error si el usuario no está en una habitación."""
    with pytest.raises(ValueError, match="User is not in a room."):
        traverse_exit(room_repository, user_not_in_room, exit_name="To Kitchen")


def test_traverse_exit_invalid_exit_name(room_repository: MemoryRoomRepository, user_in_room: User):
    """Test para verificar que se lanza un error si el nombre de la salida no existe en la habitación actual."""
    with pytest.raises(ValueError, match="An exit with that name was not found in the room."):
        traverse_exit(room_repository, user_in_room, exit_name="Invalid Exit")
