from architext.chatbot.handlers_for_core.notify_other_entered_room import notify_other_entered_room_factory
from architext.chatbot.handlers_for_core.notify_other_left_room import notify_other_left_room_factory
from architext.chatbot.ports.messaging_channel import MessagingChannel
from architext.core.domain.events import ShouldNotifyUserEnteredRoom, ShouldNotifyUserLeftRoom

def build_handlers_for_core(channel: MessagingChannel):
    EXTRA_HANDLERS_FOR_CORE = {
        ShouldNotifyUserEnteredRoom: [notify_other_entered_room_factory(channel)],
        ShouldNotifyUserLeftRoom: [notify_other_left_room_factory(channel)],
    }
    return EXTRA_HANDLERS_FOR_CORE