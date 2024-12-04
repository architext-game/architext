import pytest
from architext.clean.domain.entities.room import Room
from architext.clean.domain.entities.exit import Exit
from architext.clean.domain.unit_of_work.fake_unit_of_work import FakeUnitOfWork
from architext.clean.domain.services.add_exit_to_room.add_exit_to_room import add_exit_to_room


@pytest.fixture
def uow() -> FakeUnitOfWork:
    """Crea un repositorio de habitaciones en memoria limpio para cada prueba."""
    uow = FakeUnitOfWork()
    uow.rooms.save_room(Room(id="room1", name="Living Room", description="A cozy living room", exits=[]))
    uow.rooms.save_room(Room(id="room2", name="Kitchen", description="A modern kitchen", exits=[]))
    return uow


def test_add_exit_to_room_success(uow: FakeUnitOfWork):
    add_exit_to_room(
        uow=uow,
        id="room1",
        exit_name="To Kitchen",
        destination_room_id="room2"
    )

    room = uow.rooms.get_room_by_id("room1")
    assert uow.committed
    assert len(room.exits) == 1
    assert room.exits[0].name == "To Kitchen"
    assert room.exits[0].destination_room_id == "room2"
    assert room.exits[0].description == ""
    assert room.exits[0].is_open is True
    assert room.exits[0].visibility == "listed"


def test_add_exit_to_room_invalid_room(uow: FakeUnitOfWork):
    with pytest.raises(KeyError):
        add_exit_to_room(
            uow=uow,
            id="room3",  
            exit_name="To Nowhere",
            destination_room_id="room2"
        )
    assert not uow.committed


@pytest.mark.skip(reason="to do")
def test_add_exit_to_room_empty_fields(uow: FakeUnitOfWork):
    with pytest.raises(ValueError):
        add_exit_to_room(
            uow=uow,
            id="room1",
            exit_name="",
            destination_room_id="room2"
        )
    assert not uow.committed

    with pytest.raises(ValueError):
        add_exit_to_room(
            uow=uow,
            id="room1",
            exit_name="To Kitchen",
            destination_room_id=""
        )
    assert not uow.committed


@pytest.mark.skip(reason="to do")
def test_add_exit_to_room_duplicate_exit_name(uow: FakeUnitOfWork):
    add_exit_to_room(
        uow=uow,
        id="room1",
        exit_name="To Kitchen",
        destination_room_id="room2"
    )

    with pytest.raises(ValueError):
        add_exit_to_room(
            uow=uow,
            id="room1",
            exit_name="To Kitchen",
            destination_room_id="room3"
        )
    assert not uow.committed
