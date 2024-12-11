from . import verb
from .. import entities
import textwrap

class Who(verb.Verb):
    """Show a list of connected players"""

    command = _('who')
    verbtype = verb.VERSATILE

    def process(self, message):
        out_message = self.get_player_list()
        self.session.send_to_client(out_message)
        self.finish_interaction()

    def get_player_list(self):
        connected_users = entities.User.objects(client_id__ne=None)
        at = _("at")
        list_rows = [f'  {user.name: <26}  - {at} {self.get_location(user)}\n' for user in connected_users]
        users_list = ''.join(list_rows)
        out = _("Online players:\n{users_list}").format(users_list=users_list)
        return out

    def get_location(self, user):
        if user.room is None:
            return _('the lobby')
        world = user.room.world_state.get_world()
        if not world.public and not world in self.session.user.joined_worlds:
            return _('a private world')
        return world.name