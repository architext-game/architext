from typing import cast
import pytest # type: ignore
from architext.core.adapters.fake_uow import FakeUnitOfWork
from architext.core.commands import CreateItem
from pydantic import ValidationError
from architext.core import Architext
from architext.core.adapters.fake_uow import FakeUnitOfWork
from test.fixtures import createTestData


@pytest.fixture
def architext() -> Architext:
    return createTestData()


def test_create_item_success(architext: Architext) -> None:
    command = CreateItem(
        name="A box",
        description="It is very boxy",
        visibility="auto",
    )
    architext.handle(command, "oliver")

    uow = cast(FakeUnitOfWork, architext._uow)
    room = uow.rooms.get_room_by_id("olivers")
    assert room is not None
    print(room.items)
    box = room.items.get("A box")
    assert box is not None


def test_create_item_without_privileges_fails(architext: Architext):
    command = CreateItem(
        name="A box",
        description="It is very boxy",
        visibility="auto",
    )

    with pytest.raises(PermissionError, match="User is not in a world where she is authorized."):
        architext.handle(command, "alice")


def test_create_item_from_invalid_room_fails(architext: Architext):
    command = CreateItem(
        name="A box",
        description="It is very boxy",
        visibility="auto",
    )

    with pytest.raises(PermissionError):
        architext.handle(command, "charlie")


@pytest.mark.skip(reason="TODO")
def test_create_item_with_duplicated_name_fails(architext: Architext):
    command = CreateItem(
        name="A box",
        description="It is very boxy",
        visibility="auto",
    )

    architext.handle(command, "oliver")

    with pytest.raises(Exception):
        architext.handle(command, "oliver")


