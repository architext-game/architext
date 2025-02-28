from typing import Generic, TypeVar
from dataclasses import dataclass
from typing import Iterable, List, Mapping, Protocol, Type, Union
from architext.chatbot.ports.messaging_channel import MessagingChannel
from architext.core.ports.notifier import Notifier, Notification


@dataclass
class SentRecord:
    to_user_id: str
    notification: Notification

T = TypeVar("T", bound=Notification)

class FakeNotifier(Notifier):
    def __init__(self) -> None:
        self.sent: List[SentRecord] = []

    def notify(self, user_id: str, notification: Notification):
        self.sent.append(SentRecord(to_user_id=user_id, notification=notification))

    def get(self, notification_type: Type[T], user_id: str) -> List[T]:
        return [
            record.notification for record in self.sent
            if record.to_user_id == user_id
            and type(record.notification) == notification_type
        ]