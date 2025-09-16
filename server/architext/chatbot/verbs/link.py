from typing import TYPE_CHECKING
from architext.chatbot.verbs import verb
import architext.chatbot.strings as strings
from gettext import gettext as _

from architext.core.application.commands import CreateExit
from architext.core.domain.entities.room import Room
from architext.core.facade import Architext
from architext.core.application.queries.get_room_details import GetRoomDetails, RoomDetails
from architext.core.application.queries.is_name_valid import IsNameValid
from architext.core.application.queries.me import Me
from architext.core.application.settings import EXIT_NAME_MAX_LENGTH

if TYPE_CHECKING:
    from architext.chatbot.session import Session
else:
    Session = object()

class Link(verb.Verb):
    """This verb allow users to connect two existing rooms. One is the room where the user is located,
    The other room is specified through its id"""

    command = _('link')
    privileges_requirement = 'owner'

    def __init__(self, session: Session, architext: Architext):
        super().__init__(session, architext)
        self.current_process_function = self.process_first_message
    
    def process(self, message: str):
        if message == '/':
            self.session.sender.send(self.session.user_id, strings.cancelled)
            self.finish_interaction()
        else:
            self.current_process_function(message)

    def process_first_message(self, message: str):
        self.current_room = self.architext.query(GetRoomDetails(), self.session.user_id).room

        if self.current_room is None:
            self.session.sender.send(self.session.user_id, _("You are not in a room"))
            self.finish_interaction()
            return

        title = _('Linking from {user_room_name} (id {user_room_id}).').format(
            user_room_name=self.current_room.name, 
            user_room_id=self.current_room.id
        )
        body = _(
            'You are about to create an exit in your current room.\n'
            'Enter the id of the room you want to connect it to (you can check it using the "info" verb).\n\n'
            'Destination room id:'
        )
        self.session.sender.send_formatted(self.session.user_id, title, body, cancel=True)
        self.current_process_function = self.process_room_id

    def process_room_id(self, message: str):
        assert self.current_room is not None

        if not message:
            self.session.sender.send(self.session.user_id, strings.is_empty)
            return
        
        self.other_room = self.architext.query(GetRoomDetails(room_id=message), self.session.user_id).room

        if self.other_room is None:
            self.session.sender.send(self.session.user_id, strings.room_not_found)
            return

        if self.other_room.world_id != self.current_room.world_id:
            self.session.sender.send(self.session.user_id, strings.room_not_found)
            return

        out_message = _(
            'Linking with "{destination_name}" (number {destination_id}).\n'
            '  ⮕ Enter the name of the exit in {this_room_name} (number {this_room_id}) towards {destination_name} (number {destination_id})\n'
            '[Default: to {destination_name}]'
        ).format(
            destination_name=self.other_room.name,
            destination_id=self.other_room.id,
            this_room_name=self.current_room.name,
            this_room_id=self.current_room.id,
        )
        self.session.sender.send(self.session.user_id, out_message)
        self.current_process_function = self.process_here_exit_name


    def process_here_exit_name(self, message: str):
        assert self.current_room is not None
        assert self.other_room is not None

        if not message:
            message = _("to {destination_name}").format(destination_name=self.other_room.name)

        if len(message) > EXIT_NAME_MAX_LENGTH:
            self.session.sender.send(self.session.user_id, strings.too_long.format(limit=EXIT_NAME_MAX_LENGTH))
            return

        if self.architext.query(IsNameValid(name=message, in_room_id=self.current_room.id), self.session.user_id).error == 'duplicated':
            self.session.sender.send(self.session.user_id, strings.room_name_clash)
            return

        self.exit_from_current_room_name = message

        out_message = _(
            '  ⮕ Enter the name of the exit in {destination_name} (number {destination_id}) towards {this_room_name} (number {this_room_id})\n'
            '[Default: to {this_room_name}]'
        ).format(
            destination_name=self.other_room.name, 
            destination_id=self.other_room.id, 
            this_room_name=self.current_room.name, 
            this_room_id=self.current_room.id,
        )
        
        self.session.sender.send(self.session.user_id, out_message)
        self.current_process_function = self.process_there_exit_name


    def process_there_exit_name(self, message: str):
        assert self.current_room is not None
        assert self.other_room is not None

        if not message:
            message = _("to {destination_name}").format(destination_name=self.current_room.name)

        if len(message) > EXIT_NAME_MAX_LENGTH:
            self.session.sender.send(self.session.user_id, strings.too_long.format(limit=EXIT_NAME_MAX_LENGTH))
            return

        if self.architext.query(IsNameValid(name=message, in_room_id=self.other_room.id), self.session.user_id).error == 'duplicated':
            self.session.sender.send(self.session.user_id, strings.room_name_clash)
            return

        self.exit_from_other_room_name = message

        self.architext.handle(CreateExit(
            in_room_id=self.current_room.id,
            name=self.exit_from_current_room_name,
            description=_("It's nothing special."),
            visibility="auto",
            destination_room_id=self.other_room.id,
        ), self.session.user_id)

        self.architext.handle(CreateExit(
            in_room_id=self.other_room.id,
            name=self.exit_from_other_room_name,
            description=_("It's nothing special."),
            visibility="auto",
            destination_room_id=self.current_room.id,
        ), self.session.user_id)

        self.session.sender.send(self.session.user_id, _("Your new exits are ready!"))

        user = self.architext.query(Me(), self.session.user_id)

        self.session.sender.send_to_others_in_room(
            self.session.user_id,
            _("{user_name}'s eyes turn blank for a moment. A new exit appears in this room.")
                .format(user_name=user.name)
        )

        self.finish_interaction()
