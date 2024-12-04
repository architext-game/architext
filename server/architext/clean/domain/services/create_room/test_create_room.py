import pytest
from architext.clean.domain.unit_of_work.fake_unit_of_work import FakeUnitOfWork
from architext.clean.domain.services.create_room.create_room import create_room


@pytest.fixture
def uow() -> FakeUnitOfWork:
    return FakeUnitOfWork()


def test_create_room_success(uow: FakeUnitOfWork):
    room_id = create_room(
        uow=uow,
        name="Living Room",
        id="room1",
        description="A cozy living room"
    )

    saved_room = uow.rooms.get_room_by_id("room1")
    assert uow.committed
    assert saved_room.id == "room1"
    assert saved_room.name == "Living Room"
    assert saved_room.description == "A cozy living room"
    assert room_id == "room1"

@pytest.mark.skip(reason="to do")
def test_create_room_duplicate_id(uow: FakeUnitOfWork):
    create_room(
        uow=uow,
        name="Living Room",
        id="room1",
        description="A cozy living room"
    )

    with pytest.raises(KeyError):
        create_room(
            uow=uow,
            name="Kitchen",
            id="room1",  # Mismo ID
            description="A modern kitchen"
        )
    assert not uow.committed

@pytest.mark.skip(reason="to do")
def test_create_room_empty_fields(uow: FakeUnitOfWork):
    with pytest.raises(ValueError):
        create_room(
            uow=uow,
            name="",
            id="room1",
            description="Description without a name"
        )
    assert not uow.committed

    with pytest.raises(ValueError):
        create_room(
            uow=uow,
            name="Living Room",
            id="",
            description="Description without an ID"
        )
    assert not uow.committed

    with pytest.raises(ValueError):
        create_room(
            uow=uow,
            name="Living Room",
            id="room1",
            description=""
        )
    assert not uow.committed


def test_create_room_list_rooms(uow: FakeUnitOfWork):
    create_room(
        uow=uow,
        name="Living Room",
        id="room1",
        description="A cozy living room"
    )
    create_room(
        uow=uow,
        name="Kitchen",
        id="room2",
        description="A modern kitchen"
    )

    rooms = uow.rooms.list_rooms()
    assert len(rooms) == 2
    assert rooms[0].id == "room1"
    assert rooms[1].id == "room2"
