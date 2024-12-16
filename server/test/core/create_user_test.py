import pytest # type: ignore
from architext.adapters.fake_uow import FakeUnitOfWork
from architext.core.services.create_user import create_user
from architext.core.commands import CreateUser, CreateUserResult
from pydantic import ValidationError

from architext.core.messagebus import MessageBus
from architext.adapters.fake_notificator import FakeNotificator
from architext.adapters.fake_uow import FakeUnitOfWork
from architext.ports.unit_of_work import UnitOfWork
import pytest # type: ignore
from architext.core.commands import CreateInitialData
from architext.core.domain.entities.room import DEFAULT_ROOM


@pytest.fixture
def uow() -> FakeUnitOfWork:
    uow = FakeUnitOfWork()
    MessageBus().handle(uow, CreateInitialData())
    uow.committed = False
    return uow

@pytest.fixture
def message_bus() -> MessageBus:
    return MessageBus() 


def test_create_user_success(uow: FakeUnitOfWork, message_bus: MessageBus):
    command = CreateUser(
        name="John Doe",
        email="john.doe@example.com",
        password="securepassword123"
    )
    out = message_bus.handle(uow, command)
    
    assert type(out) is CreateUserResult
    result: CreateUserResult = out
    assert uow.committed
    assert result.user_id is not None
    saved_user = uow.users.get_user_by_id(result.user_id)
    assert saved_user is not None
    assert saved_user.name == command.name
    assert saved_user.email == command.email
    assert saved_user.match_password(command.password)


def test_create_user_missing_fields(uow: FakeUnitOfWork, message_bus: MessageBus):
    with pytest.raises(ValidationError):
        command = CreateUser(name="", email="john.doe@example.com", password="123")
        message_bus.handle(uow, command)
    assert not uow.committed

    with pytest.raises(ValidationError):
        command = CreateUser(name="John Doe", email="", password="123")
        message_bus.handle(uow, command)
    assert not uow.committed

    with pytest.raises(ValidationError):
        command = CreateUser(name="John Doe", email="john.doe@example.com", password="")
        create_user(uow, command)
    assert not uow.committed

@pytest.mark.skip(reason="to do")
def test_create_user_duplicate_name(uow: FakeUnitOfWork, message_bus: MessageBus):
    command = CreateUser(
        name="John Doe",
        email="john.doe@example.com",
        password="securepassword123"
    )
    message_bus.handle(uow, command)

    with pytest.raises(KeyError):
        command = CreateUser(
            name="John Doe",
            email="john.doe2@example.com",
            password="anotherpassword"
        )
        message_bus.handle(uow, command)
    assert not uow.committed


def test_create_user_list_users(uow: FakeUnitOfWork, message_bus: MessageBus):
    message_bus.handle(
        uow=uow,
        command=CreateUser(
            name="Alice",
            email="alice@example.com",
            password="password123"
        )
    )
    message_bus.handle(
        uow=uow,
        command=CreateUser(
            name="Bob",
            email="bob@example.com",
            password="password456"
        )
    )

    users = uow.users.list_users()
    assert len(users) == 2
    user_names = [user.name for user in users]
    assert "Alice" in user_names
    assert "Bob" in user_names
