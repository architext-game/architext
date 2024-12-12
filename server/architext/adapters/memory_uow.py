from architext.adapters.fake_notificator import FakeNotificator
from architext.adapters.memory_room_repository import MemoryRoomRepository
from architext.adapters.memory_user_repository import MemoryUserRepository
from architext.core.messagebus import MessageBus
from architext.ports.unit_of_work import UnitOfWork


class MemoryUnitOfWork(UnitOfWork):
    def __init__(self, messagebus: MessageBus = MessageBus()):
        self.committed = False
        self.rooms = MemoryRoomRepository()
        self.users = MemoryUserRepository()
        self.notifications: FakeNotificator = FakeNotificator()
        self.messagebus = MessageBus()

    def _commit(self):
        self.committed = True

    def __enter__(self):
        self.committed = False

    def rollback(self):
        pass
    