from architext.ports.unit_of_work import UnitOfWork
from architext.core.commands import Login, LoginResult

def login(uow: UnitOfWork, command: Login, client_user_id: str = "") -> LoginResult:
    with uow:
        user = uow.users.get_user_by_email(command.email)
        if user is None:
            raise ValueError("User does not exist")
        success = user.match_password(command.password)
        if not success:
            raise ValueError("Password or email are not correct")
        uow.commit()
        return LoginResult(user_id=user.id)
