from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from architext.core.ports.unit_of_work import UnitOfWork
else:
    UnitOfWork = object()

def assertUserIsLoggedIn(uow: UnitOfWork, user_id: str):
    if not isUserLoggedIn(uow, user_id):
        raise Exception("You need to be authenticated")

def isUserLoggedIn(uow: UnitOfWork, user_id: str) -> bool:
    user = uow.users.get_user_by_id(user_id)
    return user is not None

def isUserAuthorizedInCurrentWorld(uow: UnitOfWork, user_id: str) -> bool:
    user = uow.users.get_user_by_id(user_id)
    if user is None or user.room_id is None:
        return False
    
    room = uow.rooms.get_room_by_id(user.room_id)
    if room is None:
        return False

    return isUserAuthorizedInWorld(uow, user_id, room.world_id)

def isUserAuthorizedInWorld(uow: UnitOfWork, user_id: str, world_id: str) -> bool:
    world = uow.worlds.get_world_by_id(world_id)
    if world is None:
        return False

    return user_id == world.owner_user_id


class AuthorizationManager:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    def isUserAuthorizedInCurrentWorld(self, user_id: str) -> bool:
        return isUserAuthorizedInCurrentWorld(self._uow, user_id)

    def isUserAuthorizedInWorld(self, user_id: str, world_id: str) -> bool:
        return isUserAuthorizedInWorld(self._uow, user_id, world_id)
