from . import verb
from ..util import possible_meanings
from ..entities import User
import functools
import textwrap

class WorldInfo(verb.Verb):
    command = 'info mundo'

    def process(self, message):
        self.show_world_info()
        self.finish_interaction()

    def show_world_info(self):
        world = self.session.user.room.world_state.get_world()
        
        if world.editors:
            editor_names = functools.reduce(lambda a,b: '{}, {}'.format(a,b), [editor.name for editor in world.editors])
        else:
            editor_names = 'No tiene'
        message = textwrap.dedent(f'''
            Nombre del mundo: {world.name}
            Creador: {world.creator.name}
            Editores: {editor_names}
            Edición libre: {world.all_can_edit}
            El mundo es {"público" if world.public else "privado"}
            Código de invitación: {world.id}
        ''')
        self.session.send_to_client(message)


class Info(verb.Verb):
    """Shows all info of a room or item. This command is designed for creators, since it shows
    info that should be secret."""

    command = 'info'
    permissions = verb.PRIVILEGED

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

        exit_list = []
        for exit in self.session.user.room.exits:
            exit_list.append(f'   "{exit.name}" lleva a "{exit.destination.name}" ({self.visible_output(exit)})')
        exit_string = '\n'.join(exit_list)

        item_list = []
        for item in self.session.user.room.items:
            item_list.append(f'   {item.name} ({self.visible_output(item)})')
        item_string = '\n'.join(item_list)
        
        players_online = ', '.join(['{}'.format(user.name) for user in User.objects(room=self.session.user.room, client_id__ne=None)])
        players_offline = ', '.join(['{}'.format(user.name) for user in User.objects(room=self.session.user.room, client_id=None)])
        message = (f"""
Sala: "{room_name}"
{chr(9472)*(8+len(room_name))}
 Alias: {alias}
 Descripción: {description}
 Salidas:
{exit_string}
 Objetos:
{item_string}
 Jugadores online aquí: {players_online}
 Jugadores offline aquí: {players_offline}""")
        self.session.send_to_client(message)

    def visible_output(self, item):
        if item.visible == 'takable':
            return 'cogible'
        if item.visible=='obvious':
            return 'visible'
        if item.visible=='listed':
            return 'listado'
        if item.visible=='hidden':
            return 'oculto'