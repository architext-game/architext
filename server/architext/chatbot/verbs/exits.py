from architext.core.application.queries.get_current_room import GetCurrentRoom
from .verb import Verb
from gettext import gettext as _

class Exits(Verb):
    """This verb shows users all exits that are not hidden"""
    command = _('exits')

    def process(self, message: str):
        room = self.architext.query(GetCurrentRoom(), self.session.user_id).current_room

        if room is None:
            self.session.sender.send(self.session.user_id, _("You are not in a room, can't go anywhere :("))
            self.finish_interaction()
            return

        exits_names = [exit.name for exit in room.exits]

        if exits_names:
            out_message =_('Obvious exits:') + '\n ⮕ ' + '\n ⮕ '.join(exits_names)
        else:
            out_message = _('There is not an obvious way to exit this room.')

        self.session.sender.send(self.session.user_id, out_message)
        self.finish_interaction()