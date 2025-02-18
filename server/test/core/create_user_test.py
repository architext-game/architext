from typing import cast
import pytest # type: ignore
from architext.core.adapters.fake_uow import FakeUnitOfWork
from architext.core.adapters.sqlalchemy.uow import SQLAlchemyUnitOfWork
from architext.core.commands import CreateUser, CreateUserResult
from pydantic import ValidationError
from architext.core import Architext

from architext.core.adapters.fake_uow import FakeUnitOfWork
from test.fixtures import createTestArchitext

@pytest.fixture
def architext() -> Architext:
    return createTestArchitext()


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

    with pytest.raises(ValidationError):
        command = CreateUser(name="John Doe", email="", password="123")
        architext.handle(command)

    with pytest.raises(ValidationError):
        command = CreateUser(name="John Doe", email="john.doe@example.com", password="")
        architext.handle(command)

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
            name="Peter",
            email="peter@example.com",
            password="password123"
        )
    )

    architext.handle(
        command=CreateUser(
            name="Ulric",
            email="ulric@example.com",
            password="password456"
        )
    )

    with architext._uow:
        users = architext._uow.users.list_users()
        user_names = [user.name for user in users]
        print(user_names)
        assert len(users) == 10
        assert "Alice" in user_names
        assert "Bob" in user_names
