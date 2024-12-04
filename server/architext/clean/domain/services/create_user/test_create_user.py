import pytest
from architext.clean.domain.unit_of_work.fake_unit_of_work import FakeUnitOfWork
from architext.clean.domain.services.create_user.create_user import create_user

@pytest.fixture
def uow() -> FakeUnitOfWork:
    return FakeUnitOfWork()


def test_create_user_success(uow: FakeUnitOfWork):
    user_id = create_user(
        uow=uow,
        name="John Doe",
        email="john.doe@example.com",
        password="securepassword123"
    )

    # Verifica que el usuario fue guardado en el repositorio
    saved_user = uow.users.get_user_by_id(user_id)
    assert user_id is not None
    assert uow.committed
    assert saved_user.name == "John Doe"
    assert saved_user.email == "john.doe@example.com"
    assert saved_user.password_hash is not None


def test_create_user_missing_fields(uow: FakeUnitOfWork):
    with pytest.raises(ValueError, match="Name, email, and password are required"):
        create_user(uow=uow, name="", email="john.doe@example.com", password="123")
    assert not uow.committed

    with pytest.raises(ValueError, match="Name, email, and password are required"):
        create_user(uow=uow, name="John Doe", email="", password="123")
    assert not uow.committed


    with pytest.raises(ValueError, match="Name, email, and password are required"):
        create_user(uow=uow, name="John Doe", email="john.doe@example.com", password="")
    assert not uow.committed

@pytest.mark.skip(reason="to do")
def test_create_user_duplicate_name(uow: FakeUnitOfWork):
    create_user(
        uow=uow,
        name="John Doe",
        email="john.doe@example.com",
        password="securepassword123"
    )

    with pytest.raises(KeyError):
        create_user(
            uow=uow,
            name="John Doe",
            email="john.doe2@example.com",
            password="anotherpassword"
        )
    assert not uow.committed


def test_create_user_list_users(uow: FakeUnitOfWork):
    create_user(
        uow=uow,
        name="Alice",
        email="alice@example.com",
        password="password123"
    )
    create_user(
        uow=uow,
        name="Bob",
        email="bob@example.com",
        password="password456"
    )

    users = uow.users.list_users()
    assert len(users) == 2
    user_names = [user.name for user in users]
    assert "Alice" in user_names
    assert "Bob" in user_names
