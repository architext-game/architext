from typing import Dict, List
from architext.clean.domain.entities.user import User
from architext.clean.domain.repositories.user_repository import UserRepository
import copy

class MemoryUserRepository(UserRepository):
    def __init__(self):
        self._users = {}

    def get_user_by_id(self, user_id: str) -> User:
        return self._users[user_id]

    def save_user(self, user: User) -> None:
        self._users[user.id] = user

    def delete_user(self, user_id: str) -> None:
        del self._users[user_id]

    def list_users(self) -> List[User]:
        return copy.deepcopy(list(self._users.values()))