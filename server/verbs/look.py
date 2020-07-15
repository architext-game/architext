from .verb import Verb
from .util import possible_meanings
from entities import User

class Look(Verb):
    command = 'mirar'

    def process(self, message):
        command_length = len(self.command) + 1
        if message[command_length:]:
            self.show_item(message[command_length:])
        else:
            self.show_current_room()
        self.finished = True

    def show_item(self, partial_item_name):
        items_in_room = self.session.user.room.items
        names_of_items_in_room = [item.name for item in items_in_room]
        items_he_may_be_reffering_to = possible_meanings(partial_item_name, names_of_items_in_room)

        if len(items_he_may_be_reffering_to) == 1:
            item_name = items_he_may_be_reffering_to[0]
            for item in items_in_room:
                if item.name == item_name:
                    item.reload()
                    self.session.send_to_client("{}: {}".format(item_name, item.description))
                    break
        elif len(items_he_may_be_reffering_to) == 0:
            self.session.send_to_client("No ves eso por aquí.".format(partial_item_name))
        elif len(items_he_may_be_reffering_to) > 1:
            self.session.send_to_client("¿A cuál te refieres? Sé más específico.")
    
    def show_current_room(self):
        self.session.user.room.reload()
        title = self.session.user.room.name
        description = self.session.user.room.description if self.session.user.room.description else "Esta sala no tiene descripción."
        if len(self.session.user.room.exits) > 0:
            exits = '  '+('\n\r  '.join(["{}".format(exit) for exit in self.session.user.room.exits.keys()]))
            exits = "Salidas:\n\r{}".format(exits)
        else:
            exits = "No hay ningún camino para salir de esta habitación (pero podrías ser el primero en crear uno)."
        items = 'Aquí hay:\n\r  '+('\n\r  '.join(["{}".format(item.name) for item in self.session.user.room.items]))
        players_here = '\n\r'.join(['{} está aquí.'.format(user.name) for user in User.objects(room=self.session.user.room, client_id__ne=None) if user != self.session.user])
        message = "Estás en {}.\n\r{}\n\r{}\n\r{}{}".format(title, description, exits, players_here,items)
        self.session.send_to_client(message)