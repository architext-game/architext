from . import verb
from .. import entities
from . import look
import functools

class GoToLobby(verb.Verb):
    command = 'salirmundo'

    def process(self, message):
        self.session.user.room = None
        self.session.user.save()
        Lobby(self.session).show_world_list()
        self.finish_interaction()

class Lobby(verb.Verb):
    def __init__(self, session):
        super().__init__(session)
        self.current_process_function = self.process_first_message

    @classmethod
    def can_process(self, message, session):
        if session.user.room is None:
            return True
        else:
            return False

    def show_world_list(self):
        message = ""
        if entities.World.objects():
            message += 'Introduce el número del mundo al que quieras ir.\n'
            world_names_with_index = ['{}. {}  -{}'.format(index, world.name, world.creator.name) for index, world in enumerate(entities.World.objects())]
            message += functools.reduce(lambda a, b: '{}\n{}'.format(a, b), world_names_with_index)
        else:
            message += 'No hay ningún mundo en este servidor.'
        message += '\n\n+ para crear un nuevo mundo.'
        self.session.send_to_client(message)

    def process(self, message):
        self.current_process_function(message)

    def process_first_message(self, message):
        if message.isnumeric():
            self.travel_to_world(message)
        elif message == '+':
            self.create_world(message)

    def travel_to_world(self, message):
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

    def create_world(self, message):
        self.new_world = entities.World(save_on_creation=False, creator=self.session.user)
        self.session.send_to_client('Escribe el nombre que quieres ponerle al mundo.')
        self.current_process_function = self.process_word_name

    def process_word_name(self, message):
        if not message:
            self.session.send_to_client('No puede estar vacío')
            return

        self.new_world.name = message
        self.new_world.save()
        self.session.send_to_client('HECHO! Aquí lo ves:')
        self.show_world_list()
        self.finish_interaction()