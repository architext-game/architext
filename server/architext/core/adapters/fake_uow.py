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
from architext.core.ports.notifier import Notifier
from architext.core.ports.unit_of_work import UnitOfWork, Transaction
from architext.core.querymanager import QueryManager, uow_query_handlers_factory


class FakeUnitOfWork(UnitOfWork):
    def __init__(self, notifier: Notifier) -> None:
        self._transaction = Transaction(
            external_events=FakeExternalEventPublisher(self),
            missions=MemoryMissionRepository(),
            notifier=notifier,
            rooms=MemoryRoomRepository(),
            users=MemoryUserRepository(),
            worlds=MemoryWorldRepository(),
            world_templates=MemoryWorldTemplateRepository(),
            _uow=self,
        )
        self._rooms = MemoryRoomRepository()
        self._users = MemoryUserRepository()
        self._worlds = MemoryWorldRepository()
        self._world_templates = MemoryWorldTemplateRepository()
        self._missions = MemoryMissionRepository()
        self._messagebus = MessageBus()
        self._external_events = FakeExternalEventPublisher(self)
        self._notifier = FakeNotifier()
        self.queries = QueryManager(uow_query_handlers_factory(self))
        self.published_events: List[Event] = []  # to keep track of published events in tests

    def publish_events(self, events: List[Event]) -> None:
        super().publish_events(events)
        self.published_events += events

    def _commit(self):
        pass

    def __enter__(self) -> Transaction:
        return self._transaction
        # return Transaction(
        #     external_events=self._external_events,
        #     missions=self._missions,            
        #     notifier=self._notifier,
        #     rooms=self._rooms,
        #     users=self._users,
        #     worlds=self._worlds,
        #     world_templates=self._world_templates,
        #     _uow=self,
        # )

    def rollback(self):
        pass
    