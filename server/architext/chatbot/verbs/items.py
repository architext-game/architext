from architext.core.application.queries.get_current_room import GetCurrentRoom
from .verb import Verb
from gettext import gettext as _

class Items(Verb):
    """This verb shows users all items that are not hidden"""
    command = _('items')

    def process(self, message: str):
        room = self.architext.query(GetCurrentRoom(), self.session.user_id).current_room

        if room is None:
            self.session.sender.send(self.session.user_id, _("You are not in a room"))
            self.finish_interaction()
            return

        item_names = [item.name for item in room.items]

        if item_names:
            out_message = _('Obvious items:\n ● ') + f'\n {chr(9679)} '.join(item_names)
        else:
            out_message = _('At first glance, it seems there is nothing here.')

        self.session.sender.send(self.session.user_id, out_message)
        self.finish_interaction()