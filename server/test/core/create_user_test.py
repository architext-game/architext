from typing import cast
import pytest # type: ignore
from architext.core.adapters.fake_uow import FakeUnitOfWork
from architext.core.services.create_user import create_user
from architext.core.commands import CreateUser, CreateUserResult, CreateInitialData
from pydantic import ValidationError
from architext.core import Architext

from architext.core.messagebus import MessageBus
from architext.core.adapters.fake_notificator import FakeNotificator
from architext.core.adapters.fake_uow import FakeUnitOfWork
from architext.core.ports.unit_of_work import UnitOfWork
from architext.core.domain.entities.room import DEFAULT_ROOM


@pytest.fixture
def architext() -> Architext:
    uow = FakeUnitOfWork()
    MessageBus().handle(uow, CreateInitialData())
    uow.committed = False
    return Architext(uow)


def test_create_user_success(architext: Architext):
    command = CreateUser(
        name="John Doe",
        email="john.doe@example.com",
        password="securepassword123"
    )
    out = architext.handle(command)
    
    assert type(out) is CreateUserResult
    result: CreateUserResult = out
    assert cast(FakeUnitOfWork, architext._uow).committed
    assert result.user_id is not None
    saved_user = architext._uow.users.get_user_by_id(result.user_id)
    assert saved_user is not None
    assert saved_user.name == command.name
    assert saved_user.email == command.email
    assert saved_user.match_password(command.password)


def test_create_user_missing_fields(architext: Architext):
    with pytest.raises(ValidationError):
        command = CreateUser(name="", email="john.doe@example.com", password="123")
        architext.handle(command)
    assert not cast(FakeUnitOfWork, architext._uow).committed

    with pytest.raises(ValidationError):
        command = CreateUser(name="John Doe", email="", password="123")
        architext.handle(command)
    assert not cast(FakeUnitOfWork, architext._uow).committed

    with pytest.raises(ValidationError):
        command = CreateUser(name="John Doe", email="john.doe@example.com", password="")
        architext.handle(command)
    assert not cast(FakeUnitOfWork, architext._uow).committed

@pytest.mark.skip(reason="to do")
def test_create_user_duplicate_name(architext: Architext):
    command = CreateUser(
        name="John Doe",
        email="john.doe@example.com",
        password="securepassword123"
    )
    architext.handle(command)

    with pytest.raises(KeyError):
        command = CreateUser(
            name="John Doe",
            email="john.doe2@example.com",
            password="anotherpassword"
        )
        architext.handle(command)
    assert not cast(FakeUnitOfWork, architext._uow).committed


def test_create_user_list_users(architext: Architext):
    architext.handle(
        command=CreateUser(
            name="Alice",
            email="alice@example.com",
            password="password123"
        )
    )
    architext.handle(
        command=CreateUser(
            name="Bob",
            email="bob@example.com",
            password="password456"
        )
    )

    users = architext._uow.users.list_users()
    assert len(users) == 2
    user_names = [user.name for user in users]
    assert "Alice" in user_names
    assert "Bob" in user_names
