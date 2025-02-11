from gettext import gettext as _

from typing import Optional, TYPE_CHECKING

from architext.core.commands import CreateConnectedRoom
from architext.core.queries.is_name_valid import IsNameValid
from architext.core.settings import ROOM_NAME_MAX_LENGTH, ROOM_DESCRIPTION_MAX_LENGTH, EXIT_NAME_MAX_LENGTH
from architext.core import Architext
from architext.core.queries.get_current_room import CurrentRoom, GetCurrentRoom, GetCurrentRoomResult

from . import verb
import architext.chatbot.strings as strings
from dataclasses import dataclass

if TYPE_CHECKING:
    from architext.chatbot.session import Session
else:
    Session = object()

@dataclass
class BuildState():
    room_name: Optional[str] = None
    room_description: Optional[str] = None
    exit_to_new_room_name: Optional[str] = None
    exit_to_old_room_name: Optional[str] = None
    

class Build(verb.Verb):
    """This verb allows the user to create a new room connected to his current location.
    All the user need to know is the command he should write to start creation. That
    command will start a text wizard that drives him across the creation process.
    """
    command = _('build')
    permissions = verb.PRIVILEGED

    def __init__(self, session: Session, architext: Architext):
        super().__init__(session, architext)
        self.state = BuildState()
        self.current_process_function = self.process_first_message

    def process(self, message: str):
        if message == '/':
            self.session.sender.send(self.session.user_id, strings.cancelled)
            self.finish_interaction()
        else:
            self.current_process_function(message)

    def process_first_message(self, message: str):
        result = self.architext.query(GetCurrentRoom(), self.session.user_id)
        if not self.architext.authorization.isUserAuthorizedInCurrentWorld(self.session.user_id):
            self.session.sender.send(self.session.user_id, _("You can't build in a world you don't own."))
            self.finish_interaction()
            return
        if result.current_room is None:
            self.session.sender.send(self.session.user_id, _("You need to be in a room to be able to build!"))
            self.finish_interaction()
            return
        self.current_room = result.current_room

        title = _('You start building a new room.')
        body = _('Enter the following fields\n ⚑ Room\'s name')
        self.session.sender.send_formatted(self.session.user_id, title, body, cancel=True)
        self.current_process_function = self.process_room_name

    def process_room_name(self, message: str):
        if not message:
            self.session.sender.send(self.session.user_id, strings.is_empty)
        elif len(message) > ROOM_NAME_MAX_LENGTH:
            self.session.sender.send(self.session.user_id, strings.too_long.format(limit=ROOM_NAME_MAX_LENGTH))
        else:
            self.state.room_name = message
            self.session.sender.send(self.session.user_id, _(' 👁 Description  [default "{default_description}"]').format(default_description=strings.default_description))
            self.current_process_function = self.process_room_description

    def process_room_description(self, message: str):
        if not message:
            message = strings.default_description
        if len(message) > ROOM_DESCRIPTION_MAX_LENGTH:
            self.session.sender.send(self.session.user_id, strings.too_long.format(limit=ROOM_DESCRIPTION_MAX_LENGTH))
        else:
            self.state.room_description = message
            self.session.sender.send(self.session.user_id, 
                _(' ⮕ Name of the exit in "{this_room}" towards "{new_room}"\n   [Default: "to {new_room}"]')
                    .format(this_room=self.current_room.name, new_room=self.state.room_name)
            )
            self.current_process_function = self.process_here_exit_name

    def process_here_exit_name(self, message: str):
        if not message:
            message = _("to {room_name}").format(room_name=self.state.room_name)
            message = self.make_exit_name_valid(message, self.current_room)

        if len(message) > EXIT_NAME_MAX_LENGTH:
            self.session.sender.send(self.session.user_id, strings.too_long.format(limit=EXIT_NAME_MAX_LENGTH))
            return
        
        is_name_valid_result = self.architext.query(IsNameValid(name=message), self.session.user_id)

        if not is_name_valid_result.is_valid and is_name_valid_result.error == 'duplicated':
            self.session.sender.send(self.session.user_id, strings.room_name_clash)
        else:
            self.state.exit_to_new_room_name = message
            self.session.sender.send(self.session.user_id, 
                _(' ⮕ Name of the exit in "{new_room}" towards "{this_room}"\n   [Default: "to {this_room}"]')
                    .format(new_room = self.state.room_name, this_room = self.current_room.name)
            )
            self.current_process_function = self.process_there_exit_name

    def process_there_exit_name(self, message: str):
        if not message:
            message = _("to {room_name}").format(room_name=self.current_room.name)
            message = self.make_exit_name_valid(message, self.state.room_name)

        if len(message) > EXIT_NAME_MAX_LENGTH:
            self.session.sender.send(self.session.user_id, strings.too_long.format(limit=EXIT_NAME_MAX_LENGTH))
            return
        
        self.state.exit_to_old_room_name = message
        
        self.architext.handle(CreateConnectedRoom(
            name=self.state.room_name,
            description=self.state.room_description,
            exit_to_new_room_name=self.state.exit_to_new_room_name,
            exit_to_new_room_description='Nothing special about it.',
            exit_to_old_room_name=self.state.exit_to_old_room_name,
            exit_to_old_room_description='Nothing special about it.'
        ), self.session.user_id)

        self.session.sender.send(self.session.user_id, _("Your new room is ready. Good work!"))
        # if not self.session.user.master_mode:
        #     self.session.send_to_others_in_room(
        #         _("{user_name}'s eyes turn blank for a moment. A new exit appears in this room.")
        #             .format(user_name=self.session.user.name)
        #     )
        self.finish_interaction()

    def make_exit_name_valid(self, exit_name: str, room):
        return exit_name
        # while not entities.Exit.name_is_valid(exit_name, room):
        #     exit_name = _('straight {exit_name}').format(exit_name=exit_name)
        # return exit_name
