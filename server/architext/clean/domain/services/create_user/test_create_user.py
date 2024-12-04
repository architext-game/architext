import pytest
from architext.clean.domain.repositories.memory.user_repository import MemoryUserRepository
from architext.clean.domain.services.create_user.create_user import create_user

@pytest.fixture
def user_repository() -> MemoryUserRepository:
    """Crea un repositorio en memoria para pruebas."""
    return MemoryUserRepository()


def test_create_user_success(user_repository: MemoryUserRepository):
    """Test para verificar que un usuario se crea exitosamente."""
    user_name = create_user(
        user_repository=user_repository,
        name="John Doe",
        email="john.doe@example.com",
        password="securepassword123"
    )

    # Verifica que el usuario fue guardado en el repositorio
    saved_user = user_repository.get_user_by_id("John Doe")
    assert saved_user.name == "John Doe"
    assert saved_user.email == "john.doe@example.com"
    assert saved_user.password_hash is not None
    assert user_name == "John Doe"


def test_create_user_missing_fields(user_repository: MemoryUserRepository):
    """Test para verificar que falta un campo requerido."""
    with pytest.raises(ValueError, match="Name, email, and password are required"):
        create_user(user_repository, name="", email="john.doe@example.com", password="123")

    with pytest.raises(ValueError, match="Name, email, and password are required"):
        create_user(user_repository, name="John Doe", email="", password="123")

    with pytest.raises(ValueError, match="Name, email, and password are required"):
        create_user(user_repository, name="John Doe", email="john.doe@example.com", password="")

@pytest.mark.skip(reason="to do")
def test_create_user_duplicate_name(user_repository: MemoryUserRepository):
    """Test para verificar que no se sobrescriba un usuario existente con el mismo nombre."""
    create_user(
        user_repository=user_repository,
        name="John Doe",
        email="john.doe@example.com",
        password="securepassword123"
    )

    with pytest.raises(KeyError):
        create_user(
            user_repository=user_repository,
            name="John Doe",
            email="john.doe2@example.com",
            password="anotherpassword"
        )


def test_create_user_list_users(user_repository: MemoryUserRepository):
    """Test para verificar que el usuario creado aparece en la lista."""
    create_user(
        user_repository=user_repository,
        name="Alice",
        email="alice@example.com",
        password="password123"
    )
    create_user(
        user_repository=user_repository,
        name="Bob",
        email="bob@example.com",
        password="password456"
    )

    users = user_repository.list_users()
    assert len(users) == 2
    user_names = [user.name for user in users]
    assert "Alice" in user_names
    assert "Bob" in user_names
