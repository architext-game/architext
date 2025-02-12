from architext.chatbot.ports.messaging_channel import MessageOptions
from architext.core.commands import EditRoom as EditRoomCommand
from architext.core.facade import Architext
from architext.core.queries.get_room_details import GetRoomDetails
from architext.core.settings import ROOM_DESCRIPTION_MAX_LENGTH, ROOM_NAME_MAX_LENGTH
from . import verb
import architext.chatbot.strings as strings
from gettext import gettext as _
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from architext.chatbot.session import Session
else:
    Session = object()

class EditRoom(verb.Verb):
    """This verb allows users to edit properties of an item or exit that is in their current room"""

    command = _('remodel')
    privileges_requirement = 'owner'

    def __init__(self, session: Session, architext: Architext):
        super().__init__(session, architext)
        self.state: Literal['start', 'expect_option_number', 'expect_new_name', 'expect_new_description'] = 'start'

    def process(self, message: str):
        if message == '/':
            self.session.sender.send(self.session.user_id, strings.cancelled)
            self.finish_interaction()
            return
        
        if self.state == 'start':
            self.current_room = self.architext.query(GetRoomDetails(), self.session.user_id).room

            if self.current_room is None:
                self.session.sender.send(self.session.user_id, strings.room_not_found)
                self.finish_interaction()
                return

            title = _('Editing room {room_name}').format(room_name=self.current_room.name)

            body = _(
                'Enter the number of the value to edit.\n'
                '    1 - Name\n'
                '    2 - Description'
            )
            self.session.sender.send_formatted(self.session.user_id, title, body, cancel=True)
            self.state = 'expect_option_number'

        elif self.state == 'expect_option_number':
            assert self.current_room is not None

            try:
                selected_number = int(message)
            except ValueError:
                self.session.sender.send(self.session.user_id, strings.not_a_number)
                return
            
            if selected_number == 1:
                self.session.sender.send(self.session.user_id, _('Enter the new name:'), options=MessageOptions(fillInput=self.current_room.name))
                self.state = 'expect_new_name'
            elif selected_number == 2:
                self.session.sender.send(self.session.user_id, _('Enter the new description:'), options=MessageOptions(fillInput=self.current_room.description))
                self.state = 'expect_new_description'
            else:
                self.session.sender.send(self.session.user_id, _('Please enter the value of one of the options.'))

        elif self.state == 'expect_new_name':
            assert self.current_room is not None

            if len(message) == 0:
                self.session.sender.send(self.session.user_id, strings.is_empty)
                return

            if len(message) > ROOM_NAME_MAX_LENGTH:
                self.session.sender.send(self.session.user_id, strings.too_long.format(limit=ROOM_NAME_MAX_LENGTH))
                return

            self.architext.handle(EditRoomCommand(
                room_id=self.current_room.id,
                new_name=message,
            ), self.session.user_id)
            self.session.sender.send(self.session.user_id, _('Edition completed.'))
            self.finish_interaction()

        elif self.state == 'expect_new_description':
            assert self.current_room is not None

            if len(message) == 0:
                self.session.sender.send(self.session.user_id, strings.is_empty)
                return

            if len(message) > ROOM_DESCRIPTION_MAX_LENGTH:
                self.session.sender.send(self.session.user_id, strings.too_long.format(limit=ROOM_DESCRIPTION_MAX_LENGTH))
                return

            self.architext.handle(EditRoomCommand(
                room_id=self.current_room.id,
                new_description=message,
            ), self.session.user_id)
            self.session.sender.send(self.session.user_id, _('Edition completed.'))
            self.finish_interaction()
