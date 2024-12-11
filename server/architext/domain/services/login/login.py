from architext.domain.unit_of_work.unit_of_work import UnitOfWork
from pydantic import BaseModel, EmailStr, Field
from typing import Dict

class LoginInput(BaseModel):
    email: EmailStr
    password: str = Field(min_length=3, max_length=50)

class LoginOutput(BaseModel):
    user_id: str

def login(uow: UnitOfWork, input: LoginInput) -> LoginOutput:
    with uow:
        user = uow.users.get_user_by_email(input.email)
        assert user is not None
        success = user.match_password(input.password)
        if not success:
            raise ValueError("Password or email are not correct")
        uow.commit()
        return LoginOutput(user_id=user.id)
