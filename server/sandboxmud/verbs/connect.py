from . import verb
from .. import util
from .. import entities

class Connect(verb.Verb):
    """This verb allow users to connect two existing rooms. One is the room where the user is located,
    The other room is specified through its alias"""

    command = 'conectar'
    permissions = verb.PRIVILEGED

    def __init__(self, session):
        super().__init__(session)
        self.other_room = None
        self.exit_from_here = entities.Exit(room=self.session.user.room, save_on_creation=False)
        self.exit_from_there = entities.Exit(destination=self.session.user.room, save_on_creation=False)
        self.current_process_function = self.process_first_message
    
    def process(self, message):
        if message == '/':
            self.session.send_to_client("Conexión cancelada.")
            self.finish_interaction()
        else:
            self.current_process_function(message)

    def process_first_message(self, message):
        out_message = f'Conectando desde "{self.session.user.room.name}" (alias: {self.session.user.room.alias})\n{chr(9472)*(19+len(self.session.user.room.name))}\n{chr(10060)} Para cancelar, introduce "/" en cualquier momento.\n\nVas a crear una nueva salida desde esta habitación.\nDebes introducir el alias de la habitación con la que quieres conectarla.\n(Si no sabes cuál es, ve a la sala de destino y usa el comando "info" allí)\n\nAlias de destino:'
        self.session.send_to_client(out_message)
        self.current_process_function = self.process_room_alias

    def process_room_alias(self, message):
        if not message:
            self.session.send_to_client("Prueba otra vez.")
        elif entities.Room.objects(alias=message, world_state=self.session.user.room.world_state):
                self.other_room = entities.Room.objects(alias=message, world_state=self.session.user.room.world_state).first()
                self.exit_from_here.destination = self.other_room
                self.exit_from_there.room = self.other_room
                out_message =  f'Conectando con "{self.other_room.name}" (alias: {self.other_room.alias})\n'
                out_message += f' \u2B95 Introduce nombre de la salida en "{self.session.user.room.name}" hacia "{self.other_room.name}"\n[Por defecto: "a {self.other_room.name}"]'
                self.session.send_to_client(out_message)
                self.current_process_function = self.process_here_exit_name
        else:
            self.session.send_to_client("No hay ninguna sala con ese alias. Prueba otra vez.")

    def process_here_exit_name(self, message):
        if not message:
            message = "a {}".format(self.other_room.name)
            message = self.make_exit_name_valid(message, self.session.user.room)

        self.exit_from_here.name = message
        
        try:
            self.exit_from_here.ensure_i_am_valid()
        except entities.WrongNameFormat:
            self.session.send_to_client("El nombre no puede acabar con # y un número. Prueba con otro.")
        except entities.RoomNameClash:
            self.session.send_to_client("Ya hay un objeto o salida con ese nombre en esta sala. Prueba con otro.")
        except entities.TakableItemNameClash:
            self.session.send_to_client("Hay en el mundo un objeto tomable con ese nombre. Los objetos tomables deben tener un nombre único en todo el mundo, así que prueba a poner otro.")
        else:
            out_message = f' \u2B95 Introduce nombre de la salida en "{self.other_room.name}" hacia "{self.session.user.room.name}"\n[Por defecto: "a {self.session.user.room.name}"]'

            self.session.send_to_client(out_message)
            self.current_process_function = self.process_there_exit_name

    def process_there_exit_name(self, message):
        if not message:
            message = "a {}".format(self.session.user.room.name)
            message = self.make_exit_name_valid(message, self.other_room)

        self.exit_from_there.name = message

        try:
            self.exit_from_there.ensure_i_am_valid()
        except entities.WrongNameFormat:
            self.session.send_to_client("El nombre no puede acabar con # y un número. Prueba con otro.")
        except entities.RoomNameClash:
            self.session.send_to_client("Ya hay un objeto o salida con ese nombre en esta sala. Prueba con otro.")
        except entities.TakableItemNameClash:
            self.session.send_to_client("Hay en el mundo un objeto tomable con ese nombre. Los objetos tomables deben tener un nombre único en todo el mundo, así que prueba a poner otro.")
        else:
            self.exit_from_here.destination = self.other_room
            self.exit_from_there.room = self.other_room
            self.exit_from_here.save()
            self.exit_from_there.save()
            self.session.send_to_client("Conexión completada")
            if not self.session.user.master_mode:
                self.session.send_to_others_in_room("Los ojos de {} se ponen en blanco un momento. Una nueva salida aparece en la habitación.".format(self.session.user.name))
            self.finish_interaction()

    def make_exit_name_valid(self, exit_name, room):
        while not entities.Exit.name_is_valid(exit_name, room):
            exit_name = 'directo ' + exit_name
        return exit_name
