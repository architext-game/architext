from dataclasses import dataclass
from architext.core.application.commands.base import Command
from pydantic import Field, EmailStr
from architext.core.application.settings import EMAIL_MAX_LENGTH, USER_ID_MAX_LENGTH, USER_NAME_MAX_LENGTH


@dataclass
class CreateUserResult:
    user_id: str

class CreateUser(Command[CreateUserResult]):
    id: str = Field(min_length=1, max_length=USER_ID_MAX_LENGTH)
    email: EmailStr = Field(max_length=EMAIL_MAX_LENGTH)
    name: str = Field(min_length=1, max_length=USER_NAME_MAX_LENGTH) 