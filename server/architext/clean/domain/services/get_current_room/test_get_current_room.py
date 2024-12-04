import pytest
from architext.clean.domain.entities.user import User
from architext.clean.domain.entities.room import Room
from architext.clean.domain.unit_of_work.fake_unit_of_work import FakeUnitOfWork
from architext.clean.domain.services.get_current_room.get_current_room import get_current_room


@pytest.fixture
def uow() -> FakeUnitOfWork:
    """Crea un repositorio de habitaciones en memoria limpio para cada prueba."""
    uow = FakeUnitOfWork()
    uow.rooms.save_room(Room(id="room1", name="Living Room", description="A cozy living room", exits=[]))
    uow.rooms.save_room(Room(id="room2", name="Kitchen", description="A modern kitchen", exits=[]))
    return uow


@pytest.fixture
def user_in_room() -> User:
    """Crea un usuario que está en una habitación."""
    return User(id="0", name="John", email="john@example.com", room_id="room1", password_hash=b"asdasd")


@pytest.fixture
def user_not_in_room() -> User:
    """Crea un usuario que no está en ninguna habitación."""
    return User(id="1", name="Alice", email="alice@example.com", room_id=None, password_hash=b"asdasd")


def test_get_current_room_success(uow: FakeUnitOfWork, user_in_room: User):
    """Test para verificar que se obtiene correctamente la habitación actual."""
    room = get_current_room(uow=uow, user=user_in_room)

    assert room.id == "room1"
    assert room.name == "Living Room"
    assert room.description == "A cozy living room"


def test_get_current_room_user_not_in_room(uow: FakeUnitOfWork, user_not_in_room: User):
    """Test para verificar que se lanza un error si el usuario no está en una habitación."""
    with pytest.raises(ValueError, match="User is not in a room."):
        get_current_room(uow=uow, user=user_not_in_room)


def test_get_current_room_invalid_room_id(uow: FakeUnitOfWork):
    """Test para verificar que se maneja un ID de habitación inválido."""
    invalid_user = User(id="99", name="Invalid User", email="invalid@example.com", room_id="invalid_room", password_hash=b"asdasd")

    with pytest.raises(KeyError):  # Suponemos que se lanza KeyError para IDs de habitación inválidos
        get_current_room(uow=uow, user=invalid_user)
