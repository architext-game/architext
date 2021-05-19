from . import verb
from .. import entities
from . import look
import functools
import json
import textwrap
import mongoengine
import unicodedata

def remove_control_characters(s):
    return "".join(ch for ch in s if unicodedata.category(ch)[0]!="C")

class LobbyMenu(verb.Verb):
    '''Helper class that has the method that shows the lobby menu'''
    def show_lobby_menu(self):
        out_message = ""

        self.session.world_list_cache = self.get_worlds_list()

        world_list = self.session.world_list_cache
        
        if world_list:
            out_message += f'Introduce el número del mundo al que quieras ir\n'
            world_names_with_index = [f' {index}. {world.name: <36}  {world.get_connected_users()}{chr(128100)} by {world.creator.name} {"" if world.public else chr(128274)}' for index, world in enumerate(world_list)]
            out_message += functools.reduce(lambda a, b: '{}\n{}'.format(a, b), world_names_with_index)
        else:
            out_message += 'No hay ningún mundo público (o privado conocido) en este servidor.'
        out_message += textwrap.dedent('''
            
             + para crear un nuevo mundo.
             r para refrescar la lista de mundos.
             * para crear tu propia instancia de un mundo público.
             - para borrar uno de tus mundos.
             > para importar un mundo.
            Puedes introducir el código de invitación de un mundo privado para entrar en él.'''
        )
        self.session.send_to_client(out_message)

    def get_worlds_list(self):
        return list(filter(self.has_to_be_listed, entities.World.objects()))

    def has_to_be_listed(self, world):
        if world.public:
            return True
        elif world.creator == self.session.user:
            return True
        elif world in self.session.user.joined_worlds:
            return True
        else:
            return False


class GoToLobby(LobbyMenu):
    command = 'salirmundo'

    def process(self, message):
        self.session.user.leave_world()
        self.show_lobby_menu()
        self.finish_interaction()

class JoinByInviteCode(LobbyMenu):
    command = ''
    verbtype = verb.LOBBYVERB

    @classmethod
    def has_world_id_format(cls, string):
        return len(string.strip()) == 24

    @classmethod
    def can_process(cls, message, session):
        if super().can_process(message, session) and cls.has_world_id_format(message):
            return True
        else:
            return False

    def process(self, message):
        try:
            chosen_world = entities.World.objects.get(id=message)
        except entities.World.DoesNotExist:
            self.session.send_to_client("No te entiendo.")
            self.finish_interaction()
            return

        self.session.user.enter_world(chosen_world)
        
        self.session.send_to_client("VIAJANDO A {}".format(chosen_world.name))
        look.Look(self.session).show_current_room()
        self.session.send_to_others_in_room("¡Puf! {} apareció.".format(self.session.user.name))
        self.finish_interaction()

class EnterWorld(LobbyMenu):
    command = ''
    verbtype = verb.LOBBYVERB

    @classmethod
    def can_process(self, message, session):
        if super().can_process(message, session) and message.isnumeric():
            return True
        else:
            return False

    def __init__(self, session):
        super().__init__(session)
        self.current_process_function = self.process_world_number

    def process(self, message):
        self.current_process_function(message)

    def process_world_number(self, message):
        try:
            index = int(message)
        except ValueError:
            self.session.send_to_client("Introduce un número")
            self.finish_interaction()
            return
        
        try:
            chosen_world = self.session.world_list_cache[index]
        except IndexError:
            self.session.send_to_client("Introduce el número correspondiente a uno de los mundos")
            self.finish_interaction()
            return

        try:
            location_save = self.session.user.get_location_save(chosen_world)
            self.session.user.enter_world(chosen_world)
        except mongoengine.errors.DoesNotExist:
            self.session.send_to_client("Ese mundo ya no existe. Refresca el lobby escribiendo 'r'.")
            self.finish_interaction()
            return
        
        if location_save is not None:
            self.session.send_to_client("Volviendo a tu última localización en {}".format(chosen_world.name))
        else:
            self.session.send_to_client("Viajando por primera vez a {}".format(chosen_world.name))
        
        self.session.send_to_client("Pulsa enter para entrar...")
        self.current_process_function = self.enter_to_continue
        
    def enter_to_continue(self, message):
        look.Look(self.session).show_current_room()
        self.session.send_to_others_in_room("¡Puf! {} apareció.".format(self.session.user.name))
        self.finish_interaction()


class RefreshLobby(LobbyMenu):
    verbtype = verb.LOBBYVERB
    command = 'r'

    def process(self, message):
        self.show_lobby_menu()
        self.finish_interaction()

class CreateWorld(LobbyMenu):
    verbtype = verb.LOBBYVERB
    command = '+'

    def process(self, message):
        self.new_world = entities.World(save_on_creation=False, creator=self.session.user)
        self.session.send_to_client('Escribe el nombre que quieres ponerle al mundo. ("/" para cancelar)')
        self.process = self.process_word_name

    def process_word_name(self, message):
        if message == "/":
            self.session.send_to_client("Creación de mundo cancelada.")
            self.finish_interaction()
            return
        if not message:
            self.session.send_to_client('No puede estar vacío')
            return

        self.new_world.name = message
        self.new_world.save()
        self.session.send_to_client(textwrap.dedent(f'''
            Tu nuevo mundo está listo.
            Es un mundo privado{chr(128274)}. Puedes invitar a tus amigos compartiendo su código de invitación: 
            {self.new_world.id}
            Si quieres y cuando esté listo, puedes entrar en él y usar el verbo "editarmundo" para hacerlo público.'''
        ))
        self.show_lobby_menu()
        self.finish_interaction()


class DeployPublicSnapshot(LobbyMenu):
    verbtype = verb.LOBBYVERB
    command = '*'

    def process(self, message):
        self.public_snapshots = entities.WorldSnapshot.objects(public=True)

        if not self.public_snapshots:
            self.session.send_to_client('No hay mundos públicos para desplegar :(')
            self.finish_interaction()
            return

        message = '¿Qué mundo quieres desplegar? ("/" para cancelar)\n'
        for index, snapshot in enumerate(self.public_snapshots):
            message += '{}. {}\n'.format(index, snapshot.name)
        self.session.send_to_client(message)
        self.process = self.process_menu_option

    def process_menu_option(self, message):
        if message == '/':
            self.session.send_to_client('Cancelado.')
            self.show_lobby_menu()
            self.finish_interaction()
            return
            
        try:
            index = int(message)
            if index < 0:
                raise ValueError
        except ValueError:
            self.session.send_to_client("Introduce un número")
            return

        try:
            self.chosen_snapshot = self.public_snapshots[index]
        except IndexError:
            self.session.send_to_client("Introduce el número correspondiente a uno de los snapshots")
            return
        
        self.session.send_to_client('¿Cómo quieres llamar al nuevo mundo? ("/" para cancelar)')
        self.process = self.process_new_world_name

    def process_new_world_name(self, message):
        if message == "/":
            self.session.send_to_client("Cancelado")
            self.finish_interaction()
            return
        if not message:
            self.session.send_to_client('El nombre no puede estar vacío.')
            return
            
        world_name = message
        self.deploy_at_new_world(self.chosen_snapshot, world_name)
        self.session.send_to_client('Hecho.')
        self.show_lobby_menu()
        self.finish_interaction()

    def deploy_at_new_world(self, snapshot, world_name):
        snapshot_instance = snapshot.snapshoted_state.clone()
        new_world = entities.World(creator=self.session.user, world_state=snapshot_instance, name=world_name)


class DeleteWorld(LobbyMenu):
    verbtype = verb.LOBBYVERB
    command = '-'

    def process(self, message):
        self.your_worlds = entities.World.objects(creator=self.session.user)

        if not self.your_worlds:
            self.session.send_to_client("No has creado ningún mundo.")
            self.finish_interaction()
            return

        message = '¿Qué mundo quieres eliminar? ¡ES IRREVERSIBLE! ("/" para cancelar)\n'
        for index, world in enumerate(self.your_worlds):
            message += "{}. {}\n".format(index, world.name)
        self.session.send_to_client(message)
        self.process = self.process_menu_option

    def process_menu_option(self, message):
        if message == '/':
            self.session.send_to_client("Cancelado.")
            self.show_lobby_menu()
            self.finish_interaction()
            return

        try:
            index = int(message)
            if index < 0:
                raise ValueError
        except ValueError:
            self.session.send_to_client("Introduce un número")
            return

        try:
            world_to_delete = self.your_worlds[index]
        except IndexError:
            self.session.send_to_client("Introduce el número correspondiente a uno de los mundos")
            return

        try:
            world_to_delete.delete()
        except entities.CantDelete as e:
            self.session.send_to_client("No se pudo eliminar: {}".format(e))
        else:
            self.session.send_to_client("Hecho.")

        self.show_lobby_menu()
        self.finish_interaction()


class ImportWorld(LobbyMenu):
    verbtype = verb.LOBBYVERB
    command = '>'

    def process(self, message):
        self.json_message = ''
        self.new_world_state = entities.WorldState(save_on_creation=False)
        self.new_world = entities.World(save_on_creation=False, creator=self.session.user, world_state=self.new_world_state)
        self.session.send_to_client('Escribe el nombre que quieres ponerle al mundo importado. ("/" para cancelar)')
        self.process = self.process_word_name

    def process_word_name(self, message):
        if message == "/":
            self.session.send_to_client("Creación de mundo cancelada.")
            self.finish_interaction()
            return
        if not message:
            self.session.send_to_client('No puede estar vacío')
            return

        self.new_world.name = message
        self.session.send_to_client(textwrap.dedent(f'''
            Ahora pega la representación textual del mundo en un solo mensaje (obtenida mediante el comando exportar).
            Si la representación tiene muchos caracteres será dividida en vaios mensajes automáticamente. El
            servidor no considerará completada la entrada hasta que sea válida.
            Si te has equivocado al introducir la representación y quieres cancelar la importacion, envía "/".'''))
        self.process = self.process_world_json

    def process_world_json(self, message):
        # todo: check for possible risks and outcomes of bad input.
        if message == '/':
            self.session.send_to_client('Importación cancelada')
            self.show_lobby_menu()
            self.finish_interaction()
            return
        self.session.send_to_client(f"recibido un mensaje de {len(message)} caracteres")
        message_valid = False
        message_without_control_characters = remove_control_characters(message)
        self.json_message += message_without_control_characters
        try:
            world_dict = json.loads(self.json_message)
            self.session.send_to_client('Representación válida, generando mundo.')
            self.populate_world_from_dict(world_dict)
            self.session.send_to_client('Tu nuevo mundo está listo. Si en el mundo exportado había algún objeto en los inventarios de otros jugadores, estos han sido transferidos a tu inventario.')
            self.show_lobby_menu()
            self.finish_interaction()
        except json.decoder.JSONDecodeError:
            self.session.send_to_client('Mensaje procesado, representación inválida. Esperando el resto de la representación ("/" para cancelar)')
        

    def populate_world_from_dict(self, world_dict):
        items = []
        custom_verbs = []
        exits = []
        other_rooms = []
        inventories = []
        saved_items = []

        self.new_world_state.starting_room, added_items = self.room_from_dict(world_dict['starting_room'], add_world_state=False)
        items += added_items

        for room_dict in world_dict['other_rooms']:
            room, added_items = self.room_from_dict(room_dict)
            other_rooms.append(room)
            items += added_items
        
        for verb_dict in world_dict['custom_verbs']:
            custom_verbs.append(self.custom_verb_from_dict(verb_dict))

        all_rooms = other_rooms + [self.new_world_state.starting_room]
        rooms_dict_by_alias = { room.alias: room for room in all_rooms }
        for exit_dict in world_dict['exits']:
            new_exit = self.exit_from_dict(exit_dict, rooms_dict_by_alias)
            exits.append(new_exit)

        creator_inventory = self.inventory_from_dict(item_list=world_dict['inventory'], user=self.session.user)
        inventories.append(creator_inventory)

        for item_dict in world_dict['saved_items']:
            new_item = self.item_from_dict(item_dict, saved_in=self.new_world_state)
            saved_items.append(new_item)

        self.new_world_state._next_room_id = world_dict['next_room_id']

        # todo: save all in the correct order
        # save all entities that world_state references
        for verb in self.new_world_state.starting_room.custom_verbs:
            verb.save()
        self.new_world_state.starting_room.save()
        for verb in custom_verbs:
            verb.save()
        self.new_world_state.custom_verbs = custom_verbs
        # now the world state can be saved
        self.new_world_state.save()
        # now we can add the world_state reference to the starting room
        self.new_world_state.starting_room.world_state = self.new_world_state
        self.new_world_state.starting_room.save()
        # and save the saved items
        for item in saved_items:
            for verb in item.custom_verbs:
                verb.save()
            item.save()
        # now we can save the rest of the rooms
        for room in other_rooms:
            for verb in room.custom_verbs:
                verb.save()
            room.save()
        # now we can save the exits and items
        for exit in exits:
            exit.save()
        for item in items:
            for verb in item.custom_verbs:
                verb.save()
            item.save()
        # we finally save the inventories
        for inventory in inventories:
            for item in inventory.items:
                for verb in item.custom_verbs:
                    verb.save()
                item.save()
            inventory.save()
        # and the world itself
        self.new_world.save()
        


    def room_from_dict(self, room_dict, add_world_state=True):
        custom_verbs = [self.custom_verb_from_dict(verb_dict) for verb_dict in room_dict['custom_verbs']]

        new_room = entities.Room(
            save_on_creation=False, 
            world_state=self.new_world_state if add_world_state else None,
            name=room_dict['name'],
            alias=room_dict['alias'],
            description=room_dict['description'],
            custom_verbs=custom_verbs
        )

        items = []
        for item_dict in room_dict['items']:
            new_item = self.item_from_dict(item_dict, room=new_room)
            items.append(new_item)
        return new_room, items

    def item_from_dict(self, item_dict, room=None, saved_in=None):
        custom_verbs = [self.custom_verb_from_dict(verb_dict) for verb_dict in item_dict['custom_verbs']]
        
        new_item = entities.Item(
            save_on_creation=False,
            item_id=item_dict['item_id'],
            name=item_dict['name'],
            description=item_dict['description'],
            visible=item_dict['visible'],
            custom_verbs=custom_verbs,
            room=room,
            saved_in=saved_in
        )

        return new_item

    def custom_verb_from_dict(self, verb_dict):
        custom_verb = entities.CustomVerb(
            save_on_creation=False, 
            names=verb_dict["names"],
            commands=verb_dict["commands"]
        )
        return custom_verb

    def exit_from_dict(self, exit_dict, rooms_dict_by_alias):
        room_alias = exit_dict["room"]
        destination_alias = exit_dict["destination"]
        room = rooms_dict_by_alias[room_alias]
        destination = rooms_dict_by_alias[destination_alias]
        
        new_exit=entities.Exit(
            save_on_creation=False,
            name=exit_dict["name"],
            description=exit_dict["description"],
            destination=destination,
            room=room,
            visible=exit_dict['visible'],
            is_open=exit_dict['is_open'],
            key_names=exit_dict['key_names'],
        )

        return new_exit

    def inventory_from_dict(self, item_list, user):
        items = []
        for item_dict in item_list:
            new_item = self.item_from_dict(item_dict)
            items.append(new_item)
        
        new_inventory = entities.Inventory(
            save_on_creation=False,
            user=user,
            world_state=self.new_world_state,
            items=items
        )

        return new_inventory

"""
Por donde me llego:
Resulta que si el usuario mete un mensaje de mas de 4096 caracteres
ese mensaje se divide en mas mensajes mas pequeños.

Eso es un problema para el importar, ya que asume que lo va a hacer todo en el mismo mensaje.
Debemos permitir importar solo con texto, así que hay que arreglarlo.

Opcion 1: Hacer que si el mensaje se ha cortado el comando siga recibiendo mensajes y concatenandolos
hasta que salga un mensaje no cortado

    Como saber si un mensaje esta cortado?
        Si el numero de caracteres es igual al limite
            No es suficiente, porque puede tener justo ese numero de caracteres
            ¿Y cómo sabemos el limite de caracteres desde sandboxmud? No podemos hardcodearlo, hay que obtenerlo.
        + si el mensaje no está terminado (ej el json está incompleto)
            no es suficiente, porque el mensaje puede estar mal formateado desde el principio
        ¿Hay algun flag o algo que podamos obtener que nos diga que el mensaje está cortado?

Opcion 2: Añadir una cadena de texto especial al final del mensaje para marcar el final, que hasta que no
aparezca siga concatenando mensajes (como al escribir los comandos de los verbos custom).

    Hay que tener cuidado de que esa cadena de texto no pueda aparecer justo al final de un mensaje cortado
    por llegar al limite de caracteres, y que ese flag este en la descripcion de una sala, por ejemplo.
    Es un caso rarisimo, pero hay que hacer que sea un caso imposible.

Quiero permitir exportar e importar mediante texto para hacer el software muy longevo. Pero tambien quiero
poder hacerlo por archivos: 
    que al exportar se suba un archivo a anonfiles o algun sitio asi (tendría que ser asíncrono)
    Que para importar puedas dar un enlace de descarga directo donde el servidor se baje los datos (también asíncrono)


no se importa:
  X ningun objeto guardado
  X el verbo custom del mundo
    los objetos de inventario
"""