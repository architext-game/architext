from typing import Literal, TYPE_CHECKING
from architext.core.application.queries.get_current_room import GetCurrentRoom
from architext.core.application.commands import DeleteRoom
from architext.core import Architext
from . import verb
from gettext import gettext as _
if TYPE_CHECKING:
    from architext.chatbot.session import Session
else:
    Session = object()


class Raze(verb.Verb):
    """This verb allows users to delete their current room.
    A room where there are other connected players cannot be deleted.
    Also, the initial room (with alias 0) cannot be deleted.
    Note that rooms may be left disconnected after the use of this command"""

    command = _('raze')
    privileges_requirement = 'owner'

    def __init__(self, session: Session, architext: Architext):
        super().__init__(session, architext)
        self.state: Literal['start', 'await_confirmation'] = 'start'

    def process(self, message: str):
        if self.state == 'start':
            if not self.architext.authorization.isUserAuthorizedInCurrentWorld(self.session.user_id):
                self.session.sender.send(self.session.user_id, _("You can't raze in a world you don't own."))
                self.finish_interaction()
                return

            self.room = self.architext.query(GetCurrentRoom(), self.session.user_id).current_room

            if self.room is None:
                self.session.sender.send(self.session.user_id, _("You need to be in a room to do that."))
                self.finish_interaction()
                return

            self.session.sender.send(self.session.user_id, _(
                "Are you sure you want to delete room {room_name}?\n"
                "Write the room's name to confirm, / to cancel."
            ).format(
                room_name=self.room.name
            ))
            self.state = 'await_confirmation'
        elif self.state == 'await_confirmation':
            if self.room is not None and message == self.room.name:
                try:
                    self.architext.handle(DeleteRoom(), self.session.user_id)
                except ValueError:
                    self.session.sender.send(self.session.user_id, _("You can't delete this room."))

                self.session.sender.send(self.session.user_id, _("The room and the exits leading to it have been deleted."))
            else:
                self.session.sender.send(self.session.user_id, _("Deletion cancelled."))
                
            self.finish_interaction()

