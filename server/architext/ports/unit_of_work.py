from typing import Protocol, List, TYPE_CHECKING
from architext.ports.room_repository import RoomRepository
from architext.ports.user_repository import UserRepository
if TYPE_CHECKING:
    from architext.core.messagebus import MessageBus
else:
    MessageBus = object
from architext.core.domain.events import Event
from architext.ports.notificator import Notificator

class UnitOfWork(Protocol):
    messagebus: MessageBus
    rooms: RoomRepository
    users: UserRepository
    notifications: Notificator
    _events: List[Event] = []

    def __exit__(self, *args) -> None:
        self.rollback()

    def publish_events(self, events: List[Event]) -> None:
        self._events += events

    def _publish_events(self):
        for event in self._events:
            self.messagebus.handle(uow=self, event=event)
        self._events = []

    def commit(self) -> None:
        self._commit()
        self._publish_events()

    def __enter__(self, *args) -> None:
        pass

    def _commit(self) -> None:
        pass
    
    def rollback(self):
        pass