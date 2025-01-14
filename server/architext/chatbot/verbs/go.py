from gettext import gettext as _
from .verb import Verb
from .look import show_current_room
from .. import util
from .. import strings

from architext.core.commands import GetCurrentRoom, TraverseExit

class Go(Verb):
    """Allows the user to travel between rooms, using their exits."""

    command = _('go ')

    def process(self, message: str):
        command_length = len(self.command)
        partial_exit_name = message[command_length:]
        result = self.architext.handle(GetCurrentRoom(), self.session.user_id)
        
        if result.current_room is None:
            self.session.sender.send(self.session.user_id, _("You are not in a room, can't go anywhere :("))
            self.finish_interaction()
            return
        
        available_exit_names = [exit.name for exit in result.current_room.exits]
        possible_meanings = util.possible_meanings(partial_exit_name, available_exit_names)

        if len(possible_meanings) == 1:
            selected_exit_name = possible_meanings[0]
            traverse_result = self.architext.handle(TraverseExit(exit_name=selected_exit_name), self.session.user_id)
            show_current_room(
                user_id=self.session.user_id,
                sender=self.session.sender,
                architext=self.architext
            )
        elif len(possible_meanings) > 1:
            self.session.sender.send(self.session.user_id, _('There is more than one exit with a similar name. Please be more specific.'))
        elif len(possible_meanings) == 0:
            self.session.sender.send(self.session.user_id, strings.not_found)

        self.finish_interaction()
