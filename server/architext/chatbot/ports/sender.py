import abc
import typing
import dataclasses
import textwrap

from architext.core.messagebus import MessageBus
from architext.core.ports.unit_of_work import UnitOfWork
from architext.core.commands import GetCurrentRoom
from architext.chatbot import strings

@dataclasses.dataclass
class MessageOptions():
    display: typing.Literal['wrap', 'box', 'underline', 'fit'] = 'wrap'
    section: bool = True
    fillInput: typing.Optional[str] = None
    asksForPassword: bool = False

@dataclasses.dataclass
class Message():
    text: str
    options: MessageOptions

class AbstractSender(abc.ABC):
    def __init__(self, messagebus: MessageBus, uow: UnitOfWork):
        self.messagebus = messagebus
        self.uow = uow

    @abc.abstractmethod
    def _send(self, user_id: str, message: Message) -> None:
        pass

    def send_to_others_in_room(self, user_id: str, message: str, options: MessageOptions = MessageOptions(section=False)):
        result = self.messagebus.handle(self.uow, GetCurrentRoom(), user_id)
        if result.current_room is None:
            return
        for person in result.current_room.people:
            if person.id != user_id:
                self.send(person.id, message, options=options)

    def send_to_room(self, user_id: str, message, options: MessageOptions = MessageOptions(section=False)):
        result = self.messagebus.handle(self.uow, GetCurrentRoom(), user_id)
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
