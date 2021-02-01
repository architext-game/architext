from .verb import Verb
from .. import entities

class AddVerb(Verb):
    """This verb allows users to create new custom verbs tied to items.
    """

    """
    >verbo
    <sobre que objeto quieres crear el verbo?
        1: todo el mundo
        2: solo esta sala
        3: objeto 1
        4: objeto 2
        ...
        0: cancelar
    >1
    <nombre del verbo?
    ...
    """

    item_command = 'verboobjeto'  # command for adding verbs to items
    room_command = 'verbosala'    # command for adding verbs to rooms
    world_command = 'verbomundo'  # command for adding verbs to worlds

    @classmethod
    def can_process(cls, message, session):
        if message.startswith(cls.item_command) or message.startswith(cls.room_command) or message.startswith(cls.world_command):
            return True
        else:
            return False

    def __init__(self, session):
        super().__init__(session)
        self.world = None  # world on which the verb will be added, if it is a world verb
        self.room = None   # room  on which the verb will be added, if it is a room verb
        self.item = None   # item  on which the verb will be added, if it is a item verb
        self.verb_names = None
        self.command_list = []
        self.current_process_function = self.process_first_message

    def process(self, message):
        self.current_process_function(message)

    def process_first_message(self, message):
        # figure out wether it is a world, room or item verb
        if message.startswith(self.item_command):
            self.process_item_name(message)
        elif message.startswith(self.room_command):
            self.process_room_verb_creation(message)
        elif message.startswith(self.world_command):
            self.process_world_verb_creation(message)
        else:
            raise ValueError('invalid message "{}"'.format(message))

    def process_item_name(self, message):
        current_room = self.session.user.room
        target_item_name = message[len(self.item_command)+1:]

        suitable_live_item_found = next(filter(lambda i: i.name==target_item_name, current_room.items), None)
        suitable_saved_item_found = next(filter(lambda i: i.item_id==target_item_name, self.session.user.saved_items), None)
        suitable_item_found = suitable_live_item_found if suitable_live_item_found is not None else suitable_saved_item_found
        if suitable_item_found is not None:
            self.item = suitable_item_found
            self.session.send_to_client("Introduce el nombre del verbo a añadir al objeto (Ejemplos: usar, tocar, abrir, comer...) Puedes introducir varios separados por espacios.")
            self.current_process_function = self.process_verb_names
        else:
            self.session.send_to_client("No encuentras ningún objeto con ese nombre.")
            self.finish_interaction()

    def process_room_verb_creation(self, message):
        self.room = self.session.user.room
        self.session.send_to_client("Introduce el nombre del verbo a añadir a la sala (Ejemplos: usar, tocar, abrir, comer...) Puedes introducir varios separados por espacios.")
        self.current_process_function = self.process_verb_names

    def process_world_verb_creation(self, message):
        self.world = entities.World.objects[0]
        self.session.send_to_client("Introduce el nombre del verbo a añadir al mundo (Ejemplos: usar, tocar, abrir, comer...) Puedes introducir varios separados por espacios.")
        self.current_process_function = self.process_verb_names

    def process_verb_names(self, message):
        verb_names = message.split()
        if len(verb_names) == 0:
            self.session.send_to_client("Debes introducir algún nombre")
            return
        for name in verb_names:
            if not self.is_valid_verb_name(message):                
                self.session.send_to_client("En tu lista hay un nombre de verbo inválido. Vuelve a probar.")
                return
        self.verb_names = verb_names
        self.session.send_to_client("Ahora introduce la primera acción que se realizará cuando se use el verbo. Puedes usar cualquier acción que puedas usar como jugador, será como si un jugador fantasma la realizase por ti. Escribe .usuario para referirte al jugador que usa el verbo")
        self.current_process_function = self.process_command

    def process_command(self, message):
        if message == '' and len(self.command_list) > 0:
            self.build_verb()
            self.finish_interaction()
        elif self.is_valid_command(message):
            self.command_list.append(message)
            self.session.send_to_client("OK. Ahora introduce la siguiente acción o una línea vacía para terminar.")
        else:
            self.session.send_to_client("Ese comando no es válido. Prueba otra vez.")

    def build_verb(self):
        new_verb = entities.CustomVerb(names=self.verb_names, commands=self.command_list)
        if self.item is not None:
            self.item.add_custom_verb(new_verb)
            self.session.send_to_client('Verbo creado! Escribe "{} {}" para desatar su poder!'.format(self.verb_names[0], self.item.name))
        elif self.room is not None:
            self.room.add_custom_verb(new_verb)
            self.session.send_to_client('Verbo de sala creado! Escribe "{}" para desatar su poder!'.format(self.verb_names[0]))
        elif self.world is not None:
            self.world.add_custom_verb(new_verb)
            self.session.send_to_client('Verbo de sala creado! Escribe "{}" para desatar su poder!'.format(self.verb_names[0]))
        else:
            raise RuntimeError("Unreachable code reached ¯\_(ツ)_/¯")

    def is_valid_verb_name(self, name):
        # TODO checks if a name is a valid verb name
        return True

    def is_valid_command(self, command):
        # TODO checks if a command is a valid commnd
        return True
