from typing import Protocol, List, Optional
from ..entities.user import User

class UserRepository(Protocol):
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        pass

    def get_user_by_email(self, user_email: str) -> Optional[User]:
        pass

    def save_user(self, user: User) -> None:
        pass

    def delete_user(self, user_id: str) -> None:
        pass

    def list_users(self) -> List[User]:
        pass
