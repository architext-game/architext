from . import verb
from .. import entities
from . import look
import functools

class LobbyMenu(verb.Verb):
    '''Helper class that has the method that shows the lobby menu'''
    def show_lobby_menu(self):
        message = ""
        if entities.World.objects():
            message += f'Introduce el número del mundo al que quieras ir\n'
            world_names_with_index = ['{}. {: <36}  ({}) by {}'.format(index, world.name, world.get_connected_users(), world.creator.name) for index, world in enumerate(entities.World.objects())]
            message += functools.reduce(lambda a, b: '{}\n{}'.format(a, b), world_names_with_index)
        else:
            message += 'No hay ningún mundo en este servidor.'
        message += '\n\n + para crear un nuevo mundo.'
        message += '\n * para crear tu propia instancia de un mundo público.'
        message += '\n - para borrar uno de tus mundos.'
        self.session.send_to_client(message)

class GoToLobby(LobbyMenu):
    command = 'salirmundo'

    def process(self, message):
        self.session.user.room = None
        self.session.user.save()
        self.show_lobby_menu()
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

    def process(self, message):
        try:
            index = int(message)
        except ValueError:
            self.session.send_to_client("Introduce un número")
            return
        
        try:
            chosen_world = entities.World.objects[index]
        except IndexError:
            self.session.send_to_client("Introduce el número correspondiente a uno de los mundos")
            return

        self.session.user.room = chosen_world.world_state.starting_room
        self.session.user.save()
        
        self.session.send_to_client("VIAJANDO A {}".format(chosen_world.name))
        look.Look(self.session).show_current_room()
        self.session.send_to_others_in_room("¡Puf! {} apareció.".format(self.session.user.name))
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
        self.session.send_to_client('Tu nuevo mundo está listo.')
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
