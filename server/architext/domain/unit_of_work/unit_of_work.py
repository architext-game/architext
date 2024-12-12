from typing import Protocol, List
from architext.domain.repositories.room_repository import RoomRepository
from architext.domain.repositories.user_repository import UserRepository
from architext.domain.events.messagebus import MessageBus
from architext.domain.events.events import Event
from architext.domain.notifications.notification_adapter import NotificationAdapter

class UnitOfWork(Protocol):
    messagebus: MessageBus
    rooms: RoomRepository
    users: UserRepository
    notifications: NotificationAdapter
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