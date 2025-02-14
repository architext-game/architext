from gettext import gettext as _

from architext.core.queries.get_current_room import GetCurrentRoom
from architext.core.queries.get_thing_in_room import GetThingInRoom
from .verb import Verb
from .look import show_current_room
from .. import util
from .. import strings

from architext.core.commands import TraverseExit

class Go(Verb):
    """Allows the user to travel between rooms, using their exits."""

    command = _('go ')

    def process(self, message: str):
        command_length = len(self.command)
        partial_exit_name = message[command_length:]
        room_result = self.architext.query(GetCurrentRoom(), self.session.user_id)
        
        if room_result.current_room is None:
            self.session.sender.send(self.session.user_id, _("You are not in a room, can't go anywhere :("))
            self.finish_interaction()
            return
        
        exits_result = self.architext.query(GetThingInRoom(partial_name=partial_exit_name, restrict_to='exits'), self.session.user_id)

        if exits_result.status == 'exit_matched':
            assert exits_result.exit_match is not None
            selected_exit_name = exits_result.exit_match.name
            self.architext.handle(TraverseExit(exit_name=selected_exit_name), self.session.user_id)
            show_current_room(
                user_id=self.session.user_id,
                sender=self.session.sender,
                architext=self.architext
            )
        elif exits_result.status == 'multiple_matches':
            self.session.sender.send(self.session.user_id, _('There is more than one exit with a similar name. Please be more specific.'))
        elif exits_result.status == 'none_found':
            self.session.sender.send(self.session.user_id, strings.not_found)

        self.finish_interaction()
