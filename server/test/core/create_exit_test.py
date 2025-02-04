from typing import cast
import pytest # type: ignore
from architext.core.adapters.fake_uow import FakeUnitOfWork
from architext.core.services.create_user import create_user
from architext.core.commands import CreateExit, CreateUser, CreateUserResult, CreateInitialData
from pydantic import ValidationError
from architext.core import Architext

from architext.core.messagebus import MessageBus
from architext.core.adapters.fake_notificator import FakeNotificator
from architext.core.adapters.fake_uow import FakeUnitOfWork
from architext.core.ports.unit_of_work import UnitOfWork
from architext.core.domain.entities.room import DEFAULT_ROOM
from test.fixtures import createTestData


@pytest.fixture
def architext() -> Architext:
    return createTestData()


def test_create_exit_success(architext: Architext) -> None:
    command = CreateExit(
        name="A fancy door",
        description="I love this door, where may it lead to?",
        visibility="auto",
        destination_room_id="space"
    )
    architext.handle(command, "oliver")

    uow = cast(FakeUnitOfWork, architext._uow)
    room = uow.rooms.get_room_by_id("olivers")
    assert room is not None
    print(room.exits)
    exit = room.exits.get("A fancy door")
    assert exit is not None


def test_exit_to_another_world_fails(architext: Architext):
    command = CreateExit(
        name="A fancy door",
        description="I love this door, where may it lead to?",
        visibility="auto",
        destination_room_id="solitude"
    )

    with pytest.raises(ValueError, match="Cannot create an exit to a room in another world."):
        architext.handle(command, "oliver")

    uow = cast(FakeUnitOfWork, architext._uow)
    room = uow.rooms.get_room_by_id("olivers")
    assert room is not None
    exit = room.exits.get("A fancy door")
    assert exit is None


def test_create_exit_without_privileges_fails(architext: Architext):
    command = CreateExit(
        name="A fancy door",
        description="I love this door, where may it lead to?",
        visibility="auto",
        destination_room_id="solitude"
    )

    with pytest.raises(PermissionError, match="User is not in a world where she is authorized."):
        architext.handle(command, "alice")

    uow = cast(FakeUnitOfWork, architext._uow)
    room = uow.rooms.get_room_by_id("olivers")
    assert room is not None
    exit = room.exits.get("A fancy door")
    assert exit is None


def test_create_exit_from_invalid_room_fails(architext: Architext):
    command = CreateExit(
        name="A fancy door",
        description="I love this door, where may it lead to?",
        visibility="auto",
        destination_room_id="solitude"
    )

    with pytest.raises(PermissionError):
        architext.handle(command, "charlie")


def test_create_exit_to_invalid_room_fails(architext: Architext):
    command = CreateExit(
        name="A fancy door",
        description="I love this door, where may it lead to?",
        visibility="auto",
        destination_room_id="asdadas"
    )

    with pytest.raises(ValueError, match="Room with id asdadas does not exist."):
        architext.handle(command, "oliver")

    uow = cast(FakeUnitOfWork, architext._uow)
    room = uow.rooms.get_room_by_id("olivers")
    assert room is not None
    exit = room.exits.get("A fancy door")
    assert exit is None
