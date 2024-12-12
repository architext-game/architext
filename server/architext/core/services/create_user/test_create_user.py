from architext.adapters.memory_uow import MemoryUnitOfWork
from architext.core.services.create_user import CreateUserInput, create_user
import pytest
from pydantic import ValidationError

@pytest.fixture
def uow() -> MemoryUnitOfWork:
    return MemoryUnitOfWork()


def test_create_user_success(uow: MemoryUnitOfWork):
    input = CreateUserInput(
        name="John Doe",
        email="john.doe@example.com",
        password="securepassword123"
    )

    out = create_user(
        uow=uow,
        input=input
    )

    # Verifica que el usuario fue guardado en el repositorio
    saved_user = uow.users.get_user_by_id(out.user_id)
    assert out.user_id is not None
    assert uow.committed
    assert saved_user is not None
    assert saved_user.name == "John Doe"
    assert saved_user.email == "john.doe@example.com"
    assert saved_user.password_hash is not None


def test_create_user_missing_fields(uow: MemoryUnitOfWork):
    with pytest.raises(ValidationError):
        input = CreateUserInput(name="", email="john.doe@example.com", password="123")
        create_user(uow=uow, input=input)
    assert not uow.committed

    with pytest.raises(ValidationError):
        input = CreateUserInput(name="John Doe", email="", password="123")
        create_user(uow=uow, input=input)
    assert not uow.committed


    with pytest.raises(ValidationError):
        input = CreateUserInput(name="John Doe", email="john.doe@example.com", password="")
        create_user(uow=uow, input=input)
    assert not uow.committed

@pytest.mark.skip(reason="to do")
def test_create_user_duplicate_name(uow: MemoryUnitOfWork):
    input = CreateUserInput(
        name="John Doe",
        email="john.doe@example.com",
        password="securepassword123"
    )
    create_user(
        uow=uow,
        input=input
    )

    with pytest.raises(KeyError):
        input = CreateUserInput(
            name="John Doe",
            email="john.doe2@example.com",
            password="anotherpassword"
        )
        create_user(
            uow=uow,
            input=input
        )
    assert not uow.committed


def test_create_user_list_users(uow: MemoryUnitOfWork):
    create_user(
        uow=uow,
        input=CreateUserInput(
            name="Alice",
            email="alice@example.com",
            password="password123"
        )
    )
    create_user(
        uow=uow,
        input=CreateUserInput(
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
