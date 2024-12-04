from architext.clean.domain.unit_of_work.unit_of_work import UnitOfWork
from architext.clean.domain.repositories.memory.room_repository import MemoryRoomRepository
from architext.clean.domain.repositories.memory.user_repository import MemoryUserRepository


class FakeUnitOfWork(UnitOfWork):
    def __init__(self):
        self.committed = False
        self.rooms = MemoryRoomRepository()
        self.users = MemoryUserRepository()

    def commit(self):
        self.committed = True

    def __enter__(self):
        self.committed = False

    def rollback(self):
        pass
    