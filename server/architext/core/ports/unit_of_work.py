from dataclasses import dataclass, field
from typing import Generator, Literal, Optional, Protocol, List
from architext.core.ports.external_event_publisher import ExternalEventPublisher
from architext.core.ports.mission_repository import MissionRepository
from architext.core.ports.notifier import Notifier
from architext.core.ports.room_repository import RoomRepository
from architext.core.ports.user_repository import UserRepository
from architext.core.domain.events import Event
from architext.core.ports.world_repository import WorldRepository
from architext.core.ports.world_template_repository import WorldTemplateRepository
from architext.core.querymanager import QueryManager

@dataclass
class Transaction:
    rooms: RoomRepository
    users: UserRepository
    worlds: WorldRepository
    world_templates: WorldTemplateRepository
    missions: MissionRepository
    notifier: Notifier
    external_events: ExternalEventPublisher
    _uow: 'UnitOfWork'

    def publish_events(self, events: List[Event]) -> None:
        self._uow.publish_events(events)

    def commit(self) -> None:
        self._uow._commit()


class UnitOfWork(Protocol):
    queries: QueryManager
    _events: List[Event] = []

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        if exc_type is None:
            self.commit()
        else:
            self.rollback()
        # the exception will be propagated

    def __enter__(self) -> Transaction:
        pass

    def publish_events(self, events: List[Event]) -> None:
        self._events += events

    def collect_new_events(self) -> Generator[Event, None, None]:
        while len(self._events) > 0:
            yield self._events.pop()

    def commit(self) -> None:
        self._commit()

    def _commit(self) -> None:
        pass
    
    def rollback(self):
        pass