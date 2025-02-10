from architext.chatbot.ports.messaging_channel import MessagingChannel
from architext.core.domain.events import ShouldNotifyUserEnteredRoom
from architext.core.facade import Architext
from architext.core.ports.unit_of_work import UnitOfWork
from architext.chatbot.sender import Sender, MessageOptions
from gettext import gettext as _

def notify_other_entered_room_factory(channel: MessagingChannel):
    def notify_other_entered_room(uow: UnitOfWork, event: ShouldNotifyUserEnteredRoom):
        sender = Sender(channel=channel, architext=Architext(uow=uow))
        if event.entered_world:
            text = _('Poof! {user_who_entered} appeared here.').format(
                user_who_entered=event.user_name
            )
        elif event.through_exit_name is None:
            text = _('{user_who_entered} arrives from somewhere.').format(
                user_who_entered=event.user_name
            )
        else:
            text = _('{user_who_entered} arrives through {exit_name}.').format(
                user_who_entered=event.user_name,
                exit_name=event.through_exit_name
            )
        
        sender.send(
            user_id=event.to_user_id,
            message=text,
            options=MessageOptions(section=False)
        )
    
    return notify_other_entered_room
