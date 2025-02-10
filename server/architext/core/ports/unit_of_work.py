from typing import Generator, Protocol, List
from architext.core.ports.external_event_publisher import ExternalEventPublisher
from architext.core.ports.notifier import Notifier
from architext.core.ports.room_repository import RoomRepository
from architext.core.ports.user_repository import UserRepository
from architext.core.domain.events import Event
from architext.core.ports.world_repository import WorldRepository
from architext.core.ports.world_template_repository import WorldTemplateRepository
from architext.core.querymanager import QueryManager

class UnitOfWork(Protocol):
    rooms: RoomRepository
    users: UserRepository
    worlds: WorldRepository
    world_templates: WorldTemplateRepository
    queries: QueryManager
    notifier: Notifier
    external_events: ExternalEventPublisher
    _events: List[Event] = []

    def __exit__(self, *args) -> None:
        self.rollback()

    def publish_events(self, events: List[Event]) -> None:
        self._events += events

    def collect_new_events(self) -> Generator[Event, None, None]:
        while len(self._events) > 0:
            yield self._events.pop()

    def commit(self) -> None:
        self._commit()

    def __enter__(self, *args) -> None:
        pass

    def _commit(self) -> None:
        pass
    
    def rollback(self):
        pass