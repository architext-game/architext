from .verb import Verb
from util import possible_meanings
from entities import User

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

        if len(items_he_may_be_reffering_to) == 1:
            item_name = items_he_may_be_reffering_to[0]
            for item in items_in_room:
                if item.name == item_name:
                    item.reload()
                    item_description = item.description if item.description else 'no tiene nada de especial.'
                    self.session.send_to_client('Nombre del objeto: "{}"\nDescripción: "{}"\nVisible: {}'.format(item_name, item_description, item.visible))
                    break
        elif len(items_he_may_be_reffering_to) == 0:
            self.session.send_to_client("No ves eso por aquí.".format(partial_item_name))
        elif len(items_he_may_be_reffering_to) > 1:
            self.session.send_to_client("¿A cuál te refieres? Sé más específico.")
    
    def show_current_room_info(self):
        self.session.user.room.reload()
        room_name = self.session.user.room.name
        description = self.session.user.room.description
        alias = self.session.user.room.alias
        if len(self.session.user.room.exits) > 0:
            exits = '  '+('\n\r  '.join(['"{}" lleva a "{}"'.format(exit, room.name) for exit, room in self.session.user.room.exits.items()]))
            exits = "Salidas:\n\r{}".format(exits)
        else:
            exits = "No tiene salidas."
        if [item for item in self.session.user.room.items if item.visible]:
            visible_items = 'Objetos visibles: '+(', '.join(["{}".format(item.name) for item in self.session.user.room.items if item.visible]))
        else:
            visible_items = 'No hay objetos visibles.'
        if [item for item in self.session.user.room.items if not item.visible]:
            invisible_items = 'Objetos invisibles: '+(', '.join(["{}".format(item.name) for item in self.session.user.room.items if not item.visible]))
        else:
            invisible_items = 'No hay objetos invisibles'
        
        players_online = ', '.join(['"{}"'.format(user.name) for user in User.objects(room=self.session.user.room, client_id__ne=None)])
        players_offline = ', '.join(['"{}"'.format(user.name) for user in User.objects(room=self.session.user.room, client_id=None)])
        message = 'Nombre de la sala: "{name}"\nAlias: "{alias}"\nDescripción: "{description}"\n{exits}\n{visible_items}\n{invisible_items}\nJugadores online aquí: {online}\nJugadores offline aquí: {offline}'.format(
            name=room_name, alias=alias, description=description, exits=exits, visible_items=visible_items, invisible_items=invisible_items, online=players_online, offline=players_offline
        )
        self.session.send_to_client(message)