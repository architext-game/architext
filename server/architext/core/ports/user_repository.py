from typing import Protocol, List, Optional
from architext.core.domain.entities.user import User


class UserRepository(Protocol):
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        pass

    def get_user_by_email(self, user_email: str) -> Optional[User]:
        pass

    def get_user_by_name(self, username: str) -> Optional[User]:
        pass

    def save_user(self, user: User) -> None:
        pass

    def delete_user(self, user_id: str) -> None:
        pass

    def list_users(self) -> List[User]:
        pass

    def get_users_in_room(self, room_id: str) -> List[User]:
        pass
