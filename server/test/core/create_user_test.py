from typing import cast
import pytest # type: ignore
from architext.core.adapters.fake_uow import FakeUnitOfWork
from architext.core.commands import CreateUser, CreateUserResult
from pydantic import ValidationError
from architext.core import Architext
from architext.core.adapters.fake_uow import FakeUnitOfWork
from uuid import uuid4


def test_create_user_success(architext: Architext):
    command = CreateUser(
        id=str(uuid4()),
        name="John Doe",
        email="john.doe@example.com",
        password="securepassword123"
    )
    out = architext.handle(command)
    
    assert type(out) is CreateUserResult
    result: CreateUserResult = out
    assert result.user_id is not None
    with architext._uow as transaction:
        saved_user = transaction.users.get_user_by_id(result.user_id)
        assert saved_user is not None
        assert saved_user.name == command.name
        assert saved_user.email == command.email


def test_create_user_missing_fields(architext: Architext):
    with pytest.raises(ValidationError):
        command = CreateUser(id=str(uuid4()), name="", email="john.doe@example.com")
        architext.handle(command)

    with pytest.raises(ValidationError):
        command = CreateUser(id=str(uuid4()), name="John Doe", email="")
        architext.handle(command)

    with pytest.raises(ValidationError):
        command = CreateUser(id="", name="John Doe", email="john.doe@example.com")
        architext.handle(command)

@pytest.mark.skip(reason="to do")
def test_create_user_duplicate_name(architext: Architext):
    command = CreateUser(
        id=str(uuid4()),
        name="John Doe",
        email="john.doe@example.com",
        password="securepassword123"
    )
    architext.handle(command)

    with pytest.raises(KeyError):
        command = CreateUser(
            id=str(uuid4()),
            name="John Doe",
            email="john.doe2@example.com",
            password="anotherpassword"
        )
        architext.handle(command)


def test_create_user_list_users(architext: Architext):
    architext.handle(
        command=CreateUser(
            id=str(uuid4()),
            name="Peter",
            email="peter@example.com",
            password="password123"
        )
    )

    architext.handle(
        command=CreateUser(
            id=str(uuid4()),
            name="Ulric",
            email="ulric@example.com",
            password="password456"
        )
    )

    with architext._uow as transaction:
        users = transaction.users.list_users()
        user_names = [user.name for user in users]
        print(user_names)
        assert len(users) == 10
        assert "Alice" in user_names
        assert "Bob" in user_names
