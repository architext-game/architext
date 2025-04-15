from architext.core.commands import UpdateUserSettings, UpdateUserSettingsResult
from architext.core.ports.unit_of_work import UnitOfWork


class NameAlreadyTaken(Exception):
    def __init__(self, message="Name not available."):
        super().__init__(message)

def update_user_settings(uow: UnitOfWork, command: UpdateUserSettings, client_user_id: str = "") -> UpdateUserSettingsResult:
    with uow as transaction:
        user = transaction.users.get_user_by_id(user_id=client_user_id)
        if not user:
            raise PermissionError("User does not exist.")

        if command.new_name is not None:
            user_with_same_name = transaction.users.get_user_by_name(username=command.new_name)
            if user_with_same_name and user_with_same_name.id != user.id:
                raise NameAlreadyTaken()
            user.name = command.new_name
            transaction.users.save_user(user)
            
        return UpdateUserSettingsResult()
        
