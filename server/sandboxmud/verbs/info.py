from .verb import Verb
from ..util import possible_meanings
from ..entities import User

class Info(Verb):
    """Shows all info of a room or item. This command is designed for creators, since it shows
    info that should be secret."""

    command = 'info'

    def process(self, message):
        command_length = len(self.command) + 1
        if message[command_length:]:
            self.show_item_info(message[command_length:])
        else:
            self.show_current_room_info()
        self.finish_interaction()

    def show_item_info(self, partial_item_name):
        items_in_room = self.session.user.room.items
        names_of_items_in_room = [item.name for item in items_in_room]
        items_he_may_be_reffering_to = possible_meanings(partial_item_name, names_of_items_in_room)

        exits_in_room = self.session.user.room.exits
        names_of_exits_in_room = [exit.name for exit in exits_in_room]
        exits_he_may_be_reffering_to = possible_meanings(partial_item_name, names_of_exits_in_room)

        if len(items_he_may_be_reffering_to) + len(exits_he_may_be_reffering_to) == 1:
            if len(items_he_may_be_reffering_to) == 1:
                item_name = items_he_may_be_reffering_to[0]
                for item in items_in_room:
                    if item.name == item_name:
                        self.session.send_to_client('Nombre del objeto: "{}"\nDescripción: "{}"\nVisible: {}'.format(item.name, item.description, item.visible))
                        break
            else:
                exit_name = exits_he_may_be_reffering_to[0]
                for exit in exits_in_room:
                    if exit.name == exit_name:
                        self.session.send_to_client('Nombre de la salida: "{}"\nDescripción "{}"\nVisible: {}\nDestino: {} (Alias {})'.format(exit.name, exit.description, exit.visible, exit.destination.name, exit.destination.alias))
                        break

        elif len(items_he_may_be_reffering_to) + len(exits_he_may_be_reffering_to) == 0:
            self.session.send_to_client("No ves eso por aquí.".format(partial_item_name))
        elif len(items_he_may_be_reffering_to) + len(exits_he_may_be_reffering_to) > 1:
            self.session.send_to_client("¿A cuál te refieres? Sé más específico.")

    
    def show_current_room_info(self):
        room_name = self.session.user.room.name
        description = self.session.user.room.description
        alias = self.session.user.room.alias

        listed_exits = [exit for exit in self.session.user.room.exits if exit.is_listed()]
        if len(listed_exits) > 0:
            listed_exits = '  '+('\n\r  '.join(['"{}" lleva a "{}"'.format(exit.name, exit.destination.name) for exit in listed_exits]))
            listed_exits = "Salidas listadas:\n\r{}".format(listed_exits)
        else:
            listed_exits = "Salidas listadas: NINGUNA"

        obvious_exits = [exit for exit in self.session.user.room.exits if exit.is_obvious()]
        if len(obvious_exits) > 0:
            obvious_exits = '  '+('\n\r  '.join(['"{}" lleva a "{}"'.format(exit.name, exit.destination.name) for exit in obvious_exits]))
            obvious_exits = "Salidas visibles:\n\r{}".format(obvious_exits)
        else:
            obvious_exits = "Salidas visibles: NINGUNA"

        hidden_exits = [exit for exit in self.session.user.room.exits if exit.is_hidden()]
        if len(hidden_exits) > 0:
            hidden_exits = '  '+('\n\r  '.join(['"{}" lleva a "{}"'.format(exit.name, exit.destination.name) for exit in hidden_exits]))
            hidden_exits = "Salidas ocultas:\n\r{}".format(hidden_exits)
        else:
            hidden_exits = "Salidas ocultas: NINGUNA"

        if [item for item in self.session.user.room.items if item.is_listed()]:
            listed_items = 'Objetos listados: '+(', '.join(["{}".format(item.name) for item in self.session.user.room.items if item.is_listed()]))
        else:
            listed_items = 'Objetos listados: NINGUNO'

        if [item for item in self.session.user.room.items if item.is_obvious()]:
            obvious_items = 'Objetos visibles: '+(', '.join(["{}".format(item.name) for item in self.session.user.room.items if item.is_obvious()]))
        else:
            obvious_items = 'Objetos visibles: NINGUNO'

        if [item for item in self.session.user.room.items if item.is_hidden()]:
            hidden_items = 'Objetos ocultos: '+(', '.join(["{}".format(item.name) for item in self.session.user.room.items if item.is_hidden()]))
        else:
            hidden_items = 'Objetos ocultos: NINGUNO'
        
        players_online = ', '.join(['"{}"'.format(user.name) for user in User.objects(room=self.session.user.room, client_id__ne=None)])
        players_offline = ', '.join(['"{}"'.format(user.name) for user in User.objects(room=self.session.user.room, client_id=None)])
        message = 'Nombre de la sala: "{name}"\nAlias: "{alias}"\nDescripción: "{description}"\n{listed_exits}\n{obvious_exits}\n{hidden_exits}\n{listed_items}\n{obvious_items}\n{hidden_items}\nJugadores online aquí: {online}\nJugadores offline aquí: {offline}'.format(
            name=room_name, alias=alias, description=description, listed_exits=listed_exits, obvious_exits=obvious_exits, hidden_exits=hidden_exits, listed_items=listed_items, obvious_items=obvious_items, hidden_items=hidden_items, online=players_online, offline=players_offline
        )
        self.session.send_to_client(message)