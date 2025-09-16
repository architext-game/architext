"""
This module defines the UnitOfWork port, which is used as a context manager
to access all the functionality needed to alter the state of the game and
produce other side effects needed to handle commands and events, with
commit/rollback functionality.
"""

from dataclasses import dataclass
from typing import Generator, Protocol, List
from architext.core.application.ports.external_event_publisher import ExternalEventPublisher
from architext.core.application.ports.repository.missions import MissionRepository
from architext.core.application.ports.notifier import Notifier
from architext.core.application.ports.repository.rooms import RoomRepository
from architext.core.application.ports.repository.users import UserRepository
from architext.core.domain.events import Event
from architext.core.application.ports.repository.worlds import WorldRepository
from architext.core.application.ports.repository.world_templates import WorldTemplateRepository
from architext.core.application.queries.querymanager import QueryManager

@dataclass
class Transaction:
    """
    Object returned by the UnitOfWork's __enter__ method.
    It is used to access all the functionality needed to alter the state
    of the game and produce other side effects needed to handle commands and
    events. Those functions are:
    - Repositories to access and modify the game's state.
    - Notifiers to notify users of events that happened in the game.
    - ExternalEventPublisher to publish events to external systems such as
    workers executing jobs in the background.
    - The `publish_events` method to publish events that happened during the
    transaction, so they can be handled by the appropriate handlers.
    """
    rooms: RoomRepository
    users: UserRepository
    worlds: WorldRepository
    world_templates: WorldTemplateRepository
    missions: MissionRepository
    notifier: Notifier
    external_events: ExternalEventPublisher
    _uow: 'UnitOfWork'

    def publish_events(self, events: List[Event]) -> None:
        self._uow._publish_events(events)

    def commit(self) -> None:
        self._uow._commit()


class UnitOfWork(Protocol):
    """
    UnitOfWork is a context manager that can be used to access all the functionality
    needed to alter the state of the game and produce other side effects needed to
    handle commands and events, with commit/rollback functionality.
    """
    queries: QueryManager
    _events: List[Event] = []

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        if exc_type is None:
            self.commit()
        else:
            self.rollback()
        # the exception will be propagated

    def __enter__(self) -> Transaction:
        raise Exception("UnitOfWork __enter__ method not implemented, cannot be used as a context manager.")

    def _publish_events(self, events: List[Event]) -> None:
        self._events += events

    def collect_new_events(self) -> Generator[Event, None, None]:
        while len(self._events) > 0:
            yield self._events.pop()

    def commit(self) -> None:
        self._commit()

    def _commit(self) -> None:
        ...
    
    def rollback(self):
        ...