from typing import List
from architext.core.adapters.fake_external_event_publisher import FakeExternalEventPublisher
from architext.core.adapters.fake_notifier import FakeNotifier
from architext.core.adapters.memory_mission_repository import MemoryMissionRepository
from architext.core.adapters.memory_world_repository import MemoryWorldRepository
from architext.core.adapters.memory_world_template_repository import MemoryWorldTemplateRepository
from architext.core.domain.events import Event
from architext.core.adapters.memory_room_repository import MemoryRoomRepository
from architext.core.adapters.memory_user_repository import MemoryUserRepository
from architext.core.messagebus import MessageBus
from architext.core.ports.unit_of_work import UnitOfWork
from architext.core.querymanager import QueryManager, uow_query_handlers_factory


class FakeUnitOfWork(UnitOfWork):
    def __init__(self) -> None:
        self.committed = False
        self.rooms = MemoryRoomRepository()
        self.users = MemoryUserRepository()
        self.worlds = MemoryWorldRepository()
        self.world_templates = MemoryWorldTemplateRepository()
        self.missions = MemoryMissionRepository()
        self.queries = QueryManager(uow_query_handlers_factory(self))
        self.messagebus = MessageBus()
        self.published_events: List[Event] = []  # to keep track of published events in tests
        self.external_events = FakeExternalEventPublisher(self)
        self.notifier = FakeNotifier()

    def publish_events(self, events: List[Event]) -> None:
        super().publish_events(events)
        self.published_events += events

    def _commit(self):
        self.committed = True

    def __enter__(self):
        self.committed = False

    def rollback(self):
        pass
    