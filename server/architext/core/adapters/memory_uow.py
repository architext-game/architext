from architext.core.adapters.fake_external_event_publisher import FakeExternalEventPublisher
from architext.core.adapters.memory_world_repository import MemoryWorldRepository
from architext.core.adapters.memory_world_template_repository import MemoryWorldTemplateRepository
from architext.core.adapters.memory_room_repository import MemoryRoomRepository
from architext.core.adapters.memory_user_repository import MemoryUserRepository
from architext.core.messagebus import MessageBus
from architext.core.ports.unit_of_work import UnitOfWork
from architext.core.querymanager import QueryManager, uow_query_handlers_factory


class MemoryUnitOfWork(UnitOfWork):
    def __init__(self):
        self.committed = False
        self.rooms = MemoryRoomRepository()
        self.users = MemoryUserRepository()
        self.worlds = MemoryWorldRepository()
        self.world_templates = MemoryWorldTemplateRepository()
        self.queries = QueryManager(uow_query_handlers_factory(self))
        self.messagebus = MessageBus()
        self.external_events = FakeExternalEventPublisher(self)

    def _commit(self):
        self.committed = True

    def __enter__(self):
        self.committed = False

    def rollback(self):
        pass
    