from typing import List

from architext.core.adapters.fake.external_event_publisher import FakeExternalEventPublisher
from architext.core.adapters.fake.notifier import FakeNotifier
from architext.core.adapters.fake.repository.missions import MemoryMissionRepository
from architext.core.adapters.fake.repository.worlds import MemoryWorldRepository
from architext.core.adapters.fake.repository.world_templates import MemoryWorldTemplateRepository
from architext.core.domain.events import Event
from architext.core.adapters.fake.repository.rooms import MemoryRoomRepository
from architext.core.adapters.fake.repository.users import MemoryUserRepository
from architext.core.application.messagebus import MessageBus
from architext.core.application.ports.notifier import Notifier
from architext.core.application.ports.unit_of_work import UnitOfWork, Transaction
from architext.core.application.queries.querymanager import QueryManager, uow_query_handlers_factory


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

    def _publish_events(self, events: List[Event]) -> None:
        super()._publish_events(events)
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
    