from architext.clean.domain.entities.user import User
from architext.clean.domain.repositories.user_repository import UserRepository

def create_user(user_repository: UserRepository, name: str, email: str, password: str) -> str:
    # Business rule: validate user inputs
    if not name or not email or not password:
        raise ValueError("Name, email, and password are required")

    password_hash = _hash_password(password)
    user = User(name=name, email=email, password_hash=password_hash)
    user_repository.save_user(user)

    return user.name

def _hash_password(password: str) -> bytes:
    import hashlib
    return hashlib.sha256(password.encode('utf-8')).digest()