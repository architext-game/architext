from typing import Protocol

class Notificator(Protocol):
    def notify_user(self, user_id: str, event: str, data: object):
        pass
