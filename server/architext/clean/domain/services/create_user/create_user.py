from architext.clean.domain.entities.user import User
from architext.clean.domain.unit_of_work.unit_of_work import UnitOfWork
import uuid

def create_user(uow: UnitOfWork, name: str, email: str, password: str) -> str:
    # Business rule: validate user inputs
    if not name or not email or not password:
        raise ValueError("Name, email, and password are required")

    password_hash = _hash_password(password)
    user = User(id=str(uuid.uuid4()), name=name, email=email, password_hash=password_hash)

    with uow:
        uow.users.save_user(user)
        uow.commit()

    return user.id

def _hash_password(password: str) -> bytes:
    import hashlib
    return hashlib.sha256(password.encode('utf-8')).digest()