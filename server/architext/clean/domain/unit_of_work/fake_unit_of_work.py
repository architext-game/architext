from architext.clean.domain.unit_of_work.unit_of_work import UnitOfWork
from architext.clean.domain.repositories.memory.room_repository import MemoryRoomRepository
from architext.clean.domain.repositories.memory.user_repository import MemoryUserRepository
from architext.clean.domain.events.messagebus import MessageBus


class FakeUnitOfWork(UnitOfWork):
    def __init__(self, messagebus: MessageBus = MessageBus({})):
        self.committed = False
        self.rooms = MemoryRoomRepository()
        self.users = MemoryUserRepository()
        self.messagebus = messagebus

    def commit(self):
        self.committed = True

    def __enter__(self):
        self.committed = False

    def rollback(self):
        pass
    