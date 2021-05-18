import functools
import textwrap
from . import verb
from .. import util
from .. import entities

class WorldInfo(verb.Verb):
    command = 'infomundo'

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
        selected_entity = util.name_to_entity(self.session, partial_item_name, loose_match=['saved_items'], substr_match=['room_items', 'inventory', 'room_exits'])

        if selected_entity == "many":
            self.session.send_to_client("Hay varios objetos o salidas con un nombre similar a ese. Intenta ser más específico.")
            self.finish_interaction()
        elif selected_entity is None:
            self.session.send_to_client("No hay ningún objeto ni salida con ese nombre en la sala.")
            self.finish_interaction()
        else:
            if isinstance(selected_entity, entities.Item):
                self.session.send_to_client(textwrap.dedent(f"""
                    Nombre del objeto: "{selected_entity.name}"
                    Descripción: "{selected_entity.description}"
                    Visible: {selected_entity.visible}"""
                ))
            elif isinstance(selected_entity, entities.Exit):
                self.session.send_to_client(textwrap.dedent(f"""
                    Nombre de la salida: "{selected_entity.name}"
                    Descripción "{selected_entity.description}"
                    Visible: {selected_entity.visible}
                    Destino: {selected_entity.destination.name} (Alias {selected_entity.destination.name})"""
                ))
            else:
                raise ValueError(f"Item or Exit expected. {type(selected_entity)} found.")

    
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
        
        players_online = ', '.join(['{}'.format(user.name) for user in entities.User.objects(room=self.session.user.room, client_id__ne=None)])
        players_offline = ', '.join(['{}'.format(user.name) for user in entities.User.objects(room=self.session.user.room, client_id=None)])
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