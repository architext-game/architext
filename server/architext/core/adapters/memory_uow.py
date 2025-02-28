from architext.core.adapters.fake_external_event_publisher import FakeExternalEventPublisher
from architext.core.adapters.fake_notifier import FakeNotifier
from architext.core.adapters.memory_world_repository import MemoryWorldRepository
from architext.core.adapters.memory_world_template_repository import MemoryWorldTemplateRepository
from architext.core.adapters.memory_room_repository import MemoryRoomRepository
from architext.core.adapters.memory_user_repository import MemoryUserRepository
from architext.core.messagebus import MessageBus
from architext.core.ports.unit_of_work import Transaction, UnitOfWork
from architext.core.querymanager import QueryManager, uow_query_handlers_factory


class MemoryUnitOfWork(UnitOfWork):
    def __init__(self) -> None:
        self.committed = False
        self._rooms = MemoryRoomRepository()
        self._users = MemoryUserRepository()
        self._worlds = MemoryWorldRepository()
        self._world_templates = MemoryWorldTemplateRepository()
        self._messagebus = MessageBus()
        self._external_events = FakeExternalEventPublisher(self)
        self._notifier = FakeNotifier()
        self.queries = QueryManager(uow_query_handlers_factory(self))

    def _commit(self) -> None:
        self.committed = True

    def __enter__(self) -> Transaction:
        self.committed = False
        return super().__enter__()

    def rollback(self):
        pass
    