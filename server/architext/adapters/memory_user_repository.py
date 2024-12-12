from typing import Dict, List, Optional
from architext.core.domain.entities.user import User
from architext.ports.user_repository import UserRepository
import copy


class MemoryUserRepository(UserRepository):
    def __init__(self) -> None:
        self._users: Dict[str, User] = {}

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        return copy.deepcopy(self._users.get(user_id, None))
    
    def get_user_by_email(self, user_email: str) -> Optional[User]:
        return copy.deepcopy(next((user for user in self._users.values() if user.email == user_email), None))

    def save_user(self, user: User) -> None:
        self._users[user.id] = copy.deepcopy(user)

    def delete_user(self, user_id: str) -> None:
        del self._users[user_id]

    def list_users(self) -> List[User]:
        return copy.deepcopy(list(self._users.values()))

    def get_users_in_room(self, room_id):
        return copy.deepcopy(list(user for user in self._users.values() if user.room_id == room_id))