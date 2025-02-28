from architext.core.domain.entities.user import User
from architext.core.domain.entities.room import DEFAULT_ROOM
from architext.core.commands import CreateUser, CreateUserResult
from architext.core.domain.events import UserCreated
from architext.core.ports.unit_of_work import UnitOfWork
import uuid
from pydantic import BaseModel, EmailStr, Field



def create_user(uow: UnitOfWork, command: CreateUser, client_user_id: str = "") -> CreateUserResult:
    user = User(id=command.id, name=command.name, email=command.email)

    with uow as transaction:
        transaction.users.save_user(user)
        transaction.publish_events([UserCreated(user_id=user.id)])

    return CreateUserResult(user_id=user.id)
