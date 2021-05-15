from .verb import Verb
from .. import util
from .. import entities

class Look(Verb):
    """Shows room and items info to players"""

    command = 'mirar'

    def process(self, message):
        command_length = len(self.command) + 1
        if message[command_length:]:
            self.show_item_or_exit(message[command_length:])
        else:
            self.show_current_room()
        self.finish_interaction()

    def show_item_or_exit(self, partial_name):
        selected_entity = util.name_to_entity(self.session, partial_name, substr_match=['room_items', 'room_exits', 'inventory'])

        if selected_entity == 'many':
            self.session.send_to_client("¿A cuál te refieres? Sé más específico (prueba a introducir el nombre más completo o a incluir mayúsuclas y acentos).")
        elif selected_entity is None:
            self.session.send_to_client("No ves eso por aquí.")
        else:
            self.session.send_to_client(f"{chr(128065)} {selected_entity.name}\n {selected_entity.description}")
    
    def show_current_room(self):
        title = self.session.user.room.name + "\n"
        description = self.session.user.room.description + "\n"

        listed_exits = [exit.name for exit in self.session.user.room.exits if exit.is_listed()]
        if len(listed_exits) > 0:
            exits = (', '.join(listed_exits))
            exits = "\u2B95 Salidas: {}.\n".format(exits)
        else:
            exits = ""

        listed_items = [item.name for item in self.session.user.room.items if item.is_listed()]
        if len(listed_items) > 0:
            items = f'{chr(128065)} Ves '+(', '.join(listed_items))
            items = items + '.\n'
        else:
            items = ''

        players_here = entities.User.objects(room=self.session.user.room, client_id__ne=None, master_mode=False)
        players_here = [user for user in players_here if user != self.session.user]
        if len(players_here) < 1:
            players_here = ""
        elif len(players_here) == 1:
            players_here = f"{players_here[0].name} está aquí"
        else:
            players_here = f"Están aquí: {', '.join([f'{user.name}' for user in players_here])}"
        players_here = f'{chr(128100)} {players_here}.' + '\n' if players_here != '' else ''
        underline = f"{chr(9472)*(len(title))}"
        message = (f"""{title}{underline}\n{description}{items}{players_here}{exits}""")
        self.session.send_to_client(message)
