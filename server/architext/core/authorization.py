from typing import TYPE_CHECKING, Optional

from architext.core.domain.entities.user import User
if TYPE_CHECKING:
    from architext.core.ports.unit_of_work import UnitOfWork, Transaction
else:
    UnitOfWork = object()
    Transaction = object()

def assertUserIsLoggedIn(transaction: Transaction, user_id: str):
    if not isUserLoggedIn(transaction, user_id):
        raise Exception("You need to be authenticated")

def assertUserIsAuthorizedInCurrentWorld(transaction: Transaction, user_id: str):
    if getUserAuthorizedInCurrentWorld(transaction, user_id) is None:
        raise PermissionError("You need to be the owner of the world to do that")

def isUserLoggedIn(transaction: Transaction, user_id: str) -> bool:
    user = transaction.users.get_user_by_id(user_id)
    return user is not None

def getUserAuthorizedInCurrentWorld(transaction: Transaction, user_id: str) -> Optional[User]:
    user = transaction.users.get_user_by_id(user_id)
    if user is None or user.room_id is None:
        return None
    
    room = transaction.rooms.get_room_by_id(user.room_id)
    if room is None:
        return None

    if not isUserAuthorizedInWorld(transaction, user_id, room.world_id):
        return None
    
    return user

def isUserAuthorizedInWorld(transaction: Transaction, user_id: str, world_id: str) -> bool:
    world = transaction.worlds.get_world_by_id(world_id)
    if world is None:
        return False

    return user_id == world.owner_user_id


class AuthorizationManager:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    def isUserAuthorizedInCurrentWorld(self, user_id: str) -> bool:
        with self._uow as transaction:
            return getUserAuthorizedInCurrentWorld(transaction, user_id) is not None

    def isUserAuthorizedInWorld(self, user_id: str, world_id: str) -> bool:
        with self._uow as transaction:
            return isUserAuthorizedInWorld(transaction, user_id, world_id)
