import abc
import textwrap

from architext.chatbot.ports.messaging_channel import MessagingChannel, Message, MessageOptions
from architext.core.facade import Architext
from architext.core.application.messagebus import MessageBus
from architext.core.application.ports.unit_of_work import UnitOfWork
from architext.core.application.queries.get_current_room import GetCurrentRoom
from architext.chatbot import strings

class Sender(abc.ABC):
    def __init__(self, channel: MessagingChannel, architext: Architext):
        self.architext = architext
        self.channel = channel

    def _send(self, user_id: str, message: Message) -> None:
        self.channel.send(user_id, message)

    def send_to_others_in_room(self, user_id: str, message: str, options: MessageOptions = MessageOptions(section=False)):
        result = self.architext.query(GetCurrentRoom(), user_id)
        if result.current_room is None:
            return
        for person in result.current_room.people:
            if person.id != user_id:
                self.send(person.id, message, options=options)

    def send_to_room(self, user_id: str, message, options: MessageOptions = MessageOptions(section=False)):
        result = self.architext.query(GetCurrentRoom(), user_id)
        if result.current_room is None:
            return
        for person in result.current_room.people:
            self.send(person.id, message, options=options)

    def send(self, user_id: str, message: str, wrap=False, options: MessageOptions = MessageOptions()):
        if wrap:
            # Wrap the message to 80 characters
            message = '\n'.join(
                # Wrap each line individually 
                ['\n'.join(textwrap.wrap(line, 80, 
                    replace_whitespace=False,
                    expand_tabs=False,
                    drop_whitespace=False,
                    break_on_hyphens=False,
                    break_long_words=False
                    ))
                for line in message.splitlines()]
            )

        self._send(user_id, message=Message(text=message, options=options))

    def send_formatted(self, user_id: str, title: str, body: str, cancel=False):
        self.send(user_id, title, options=MessageOptions(display='underline'))
        if cancel:
            self.send(user_id, strings.cancel_prompt, options=MessageOptions(section=False))
        self.send(user_id, body, options=MessageOptions(section=False))
