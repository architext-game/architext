import pytest
from architext.clean.domain.entities.user import User
from architext.clean.domain.entities.room import Room
from architext.clean.domain.repositories.memory.user_repository import MemoryUserRepository
from architext.clean.domain.repositories.memory.room_repository import MemoryRoomRepository
from architext.clean.domain.services.put_user_in_room.put_user_in_room import put_user_in_room


@pytest.fixture
def user_repository() -> MemoryUserRepository:
    repo = MemoryUserRepository()
    repo.save_user(User(name="John", email="john@example.com", room_id=None, password_hash=b"asd"))
    repo.save_user(User(name="Alice", email="alice@example.com", room_id=None, password_hash=b"asd"))
    return repo


@pytest.fixture
def room_repository() -> MemoryRoomRepository:
    repo = MemoryRoomRepository()
    repo.save_room(Room(id="room1", name="Living Room", description="A cozy living room", exits=[]))
    repo.save_room(Room(id="room2", name="Kitchen", description="A modern kitchen", exits=[]))
    return repo


def test_put_user_in_room_success(user_repository: MemoryUserRepository, room_repository: MemoryRoomRepository):
    """Test para verificar que un usuario es asignado exitosamente a una habitación."""
    put_user_in_room(user_repository, room_repository, user_id="John", room_id="room1")

    user = user_repository.get_user_by_id("John")
    assert user.room_id == "room1"


def test_put_user_in_room_invalid_room(user_repository: MemoryUserRepository, room_repository: MemoryRoomRepository):
    """Test para verificar que no se puede asignar un usuario a una habitación inexistente."""
    with pytest.raises(KeyError):
        put_user_in_room(user_repository, room_repository, user_id="John", room_id="invalid_room")


def test_put_user_in_room_invalid_user(user_repository: MemoryUserRepository, room_repository: MemoryRoomRepository):
    """Test para verificar que no se puede asignar una habitación a un usuario inexistente."""
    with pytest.raises(KeyError):
        put_user_in_room(user_repository, room_repository, user_id="invalid_user", room_id="room1")
