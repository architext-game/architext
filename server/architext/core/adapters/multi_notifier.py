from typing import Iterable, List, Mapping, Protocol, Type, Union
from architext.chatbot.adapters.chatbot_notifier import ChatbotNotifier
from architext.core.adapters.sio_notifier import SioNotifier
from architext.core.application.ports.notifier import Notifier, Notification, SocialInteractionNotification, UserEnteredRoomNotification, UserLeftRoomNotification, WorldCreatedNotification

def multi_notifier_mapping_factory(
        web: Notifier, chatbot: Notifier
) -> Mapping[Type[Notification], List[Notifier]]:
    return {
        UserEnteredRoomNotification: [chatbot],
        UserLeftRoomNotification: [chatbot],
        SocialInteractionNotification: [chatbot],
        WorldCreatedNotification: [web],
    }

class MultiNotifier(Notifier):
    def __init__(self, notifiers: Mapping[Type[Notification], List[Notifier]]) -> None:
        self.notifiers = notifiers

    def notify(self, user_id: str, notification: Notification):
        for notifier in self.notifiers.get(type(notification), []):
            notifier.notify(user_id, notification)
