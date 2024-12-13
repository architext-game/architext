from architext.core.domain.entities.user import User
from architext.core.domain.entities.room import DEFAULT_ROOM
from architext.core.commands import CreateUser, CreateUserResult
from architext.ports.unit_of_work import UnitOfWork
import uuid
from pydantic import BaseModel, EmailStr, Field



def create_user(uow: UnitOfWork, command: CreateUser, client_user_id: str = "") -> CreateUserResult:
    password_hash = _hash_password(command.password)
    user = User(id=str(uuid.uuid4()), name=command.name, email=command.email, password_hash=password_hash, room_id=DEFAULT_ROOM.id)

    with uow:
        uow.users.save_user(user)
        uow.commit()

    return CreateUserResult(user_id=user.id)

def _hash_password(password: str) -> bytes:
    import hashlib
    return hashlib.sha256(password.encode('utf-8')).digest()