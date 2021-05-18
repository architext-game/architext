from . import verb
from .. import entities
import textwrap

class Who(verb.Verb):
    """Show a list of connected players"""

    command = 'quien'
    verbtype = verb.VERSATILE

    def process(self, message):
        out_message = self.get_player_list()
        self.session.send_to_room(out_message)
        self.finish_interaction()

    def get_player_list(self):
        connected_users = entities.User.objects(client_id__ne=None)
        list_rows = [f'  {user.name}\n' for user in connected_users]
        users_list = ''.join(list_rows)
        out = textwrap.dedent(f"""
            Jugadores conectados:
            {users_list}"""
        )
        return out