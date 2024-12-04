from typing import Protocol
from architext.clean.domain.repositories.room_repository import RoomRepository
from architext.clean.domain.repositories.user_repository import UserRepository

class UnitOfWork(Protocol):
    rooms: RoomRepository
    users: UserRepository

    def __exit__(self, *args) -> None:
        self.rollback()

    def __enter__(self, *args) -> None:
        pass

    def commit(self) -> None:
        pass
    
    def rollback(self):
        pass