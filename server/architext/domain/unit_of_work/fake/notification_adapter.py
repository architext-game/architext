from typing import Protocol, Dict, List
from architext.domain.notifications.notification_adapter import NotificationAdapter as NAProtocol
from dataclasses import dataclass

@dataclass
class NotificationRecord:
    user_id: str
    event: str
    data: object

class FakeNotificationAdapter(NAProtocol):
    def __init__(self) -> None:
        self.notifications: Dict[str, List] = {}

    def notify_user(self, user_id: str, event: str, data: object):
        if self.notifications.get(user_id, None) is None:
            self.notifications[user_id] = []
            
        self.notifications[user_id].append(NotificationRecord(
            user_id=user_id,
            event=event,
            data=data
        ))
