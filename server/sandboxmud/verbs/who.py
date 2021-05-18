from . import verb
from .. import entities
import textwrap

class Who(verb.Verb):
    """Show a list of connected players"""

    command = 'quien'
    verbtype = verb.VERSATILE

    def process(self, message):
        out_message = self.get_player_list()
        self.session.send_to_client(out_message)
        self.finish_interaction()

    def get_player_list(self):
        connected_users = entities.User.objects(client_id__ne=None)
        list_rows = [f'  {user.name: <26}  - En {self.get_location(user)}\n' for user in connected_users]
        users_list = ''.join(list_rows)
        out = f"Jugadores conectados:\n{users_list}"
        return out

    def get_location(self, user):
        if user.room is None:
            return 'el lobby'
        world = user.room.world_state.get_world()
        if not world.public and not world in self.session.user.joined_worlds:
            return 'un mundo privado'
        return world.name