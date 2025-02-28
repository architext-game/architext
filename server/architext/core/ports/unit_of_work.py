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

"""
Objetivo del refactor: 
 - modifical la interfaz de unit of work para que no se puedan usar sin iniciar una transacción:
   - los repositorios
   - las queries
   - el notifier
   - los external events
 - cambiar TODAS las transacciones para hacer uso de with uow as ... para usar la nueva interfaz.
 - que la interfaz de cara al messagebus sea igual, es decir, publish events debe funcionar desde
  el uow
"""

class UnitOfWork(Protocol):
    _rooms: RoomRepository
    _users: UserRepository
    _worlds: WorldRepository
    _world_templates: WorldTemplateRepository
    _missions: MissionRepository
    queries: QueryManager
    _notifier: Notifier
    _external_events: ExternalEventPublisher
    _events: List[Event] = []

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        if exc_type is None:
            self.commit()
        else:
            self.rollback()
        # the exception will be propagated

    def __enter__(self) -> Transaction:
        return Transaction(
            external_events=self._external_events,
            missions=self._missions,
            notifier=self._notifier,
            rooms=self._rooms,
            users=self._users,
            worlds=self._worlds,
            world_templates=self._world_templates,
            _uow=self,
        )

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