from architext.domain.entities.user import User
from architext.domain.entities.room import DEFAULT_ROOM
from architext.domain.unit_of_work.unit_of_work import UnitOfWork
import uuid
from pydantic import BaseModel, EmailStr, Field

class CreateUserInput(BaseModel):
    email: EmailStr
    name: str = Field(min_length=3, max_length=10)
    password: str = Field(min_length=3, max_length=50)

class CreateUserOutput(BaseModel):
    user_id: str

def create_user(uow: UnitOfWork, input: CreateUserInput) -> CreateUserOutput:
    password_hash = _hash_password(input.password)
    user = User(id=str(uuid.uuid4()), name=input.name, email=input.email, password_hash=password_hash, room_id=DEFAULT_ROOM.id)

    with uow:
        uow.users.save_user(user)
        uow.commit()

    return CreateUserOutput(user_id=user.id)

def _hash_password(password: str) -> bytes:
    import hashlib
    return hashlib.sha256(password.encode('utf-8')).digest()