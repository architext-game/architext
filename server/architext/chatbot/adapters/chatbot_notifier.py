from architext.chatbot.ports.messaging_channel import Message, MessageOptions, MessagingChannel
from architext.core.application.ports.notifier import Notification, Notifier, SocialInteractionNotification, UserEnteredRoomNotification, UserLeftRoomNotification
from gettext import gettext as _

class ChatbotNotifier(Notifier):
    def __init__(self, channel: MessagingChannel):
        self.channel = channel

    def notify(self, user_id: str, notification: Notification):
        text = ""
        if isinstance(notification, UserEnteredRoomNotification):
            if notification.movement in ["entered_world", "teleported", "reconnected"]:
                text = _('Poof! {user_who_entered} appeared here.').format(
                    user_who_entered=notification.user_name
                )
            elif notification.through_exit_name is None:
                text = _('{user_who_entered} arrives from somewhere.').format(
                    user_who_entered=notification.user_name
                )
            else:
                text = _('{user_who_entered} arrives through {exit_name}.').format(
                    user_who_entered=notification.user_name,
                    exit_name=notification.through_exit_name
                )
            
            self.channel.send(
                user_id=user_id,
                message=Message(text=text, options=MessageOptions(section=False))
            )
        elif isinstance(notification, UserLeftRoomNotification):
            if notification.movement == 'left_world' or notification.movement == 'disconnected' or notification.movement == 'teleported':
                text = _('Swoosh! {user_who_entered} left.').format(
                    user_who_entered=notification.user_name
                )
            elif notification.movement == 'used_exit' and notification.through_exit_name is None:
                text = _('{user_who_entered} left to somewhere.').format(
                    user_who_entered=notification.user_name
                )
            elif notification.movement == 'used_exit' and notification.through_exit_name is not None:
                text = _('{user_who_entered} leaves through {exit_name}.').format(
                    user_who_entered=notification.user_name,
                    exit_name=notification.through_exit_name
                )
            
            self.channel.send(
                user_id=user_id,
                message=Message(text=text, options=MessageOptions(section=False))
            )

        elif isinstance(notification, SocialInteractionNotification):
            if notification.kind == 'talk':
                text = _('{user} says "{content}"').format(
                    user=notification.user_name,
                    content=notification.content
                )
            elif notification.kind == 'emote':
                text = _('{user} {content}').format(
                    user=notification.user_name,
                    content=notification.content
                )
            self.channel.send(
                user_id=user_id,
                message=Message(text=text, options=MessageOptions(section=False))
            )