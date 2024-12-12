from typing import Protocol

class NotificationAdapter(Protocol):
    def notify_user(self, user_id: str, event: str, data: object):
        pass
