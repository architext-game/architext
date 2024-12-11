from architext.domain.unit_of_work.unit_of_work import UnitOfWork
from architext.domain.unit_of_work.fake.room_repository import MemoryRoomRepository
from architext.domain.unit_of_work.fake.user_repository import MemoryUserRepository
from architext.domain.events.messagebus import MessageBus


class FakeUnitOfWork(UnitOfWork):
    def __init__(self, messagebus: MessageBus = MessageBus({})):
        self.committed = False
        self.rooms = MemoryRoomRepository()
        self.users = MemoryUserRepository()
        self.messagebus = messagebus

    def _commit(self):
        self.committed = True

    def __enter__(self):
        self.committed = False

    def rollback(self):
        pass
    