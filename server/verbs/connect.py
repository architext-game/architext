from .verb import Verb
import entities

class Connect(Verb):
    """This verb allow users to connect two existing rooms. One is the room where the user is located,
    The other room is specified through its alias"""

    command = 'conectar'

    def __init__(self, session):
        super().__init__(session)
        self.other_room = None
        self.exit_from_here = None
        self.exit_from_there = None
        self.current_process_function = self.process_first_message

    def process(self, message):
        self.current_process_function(message)

    def process_first_message(self, message):
        self.session.send_to_client("Vas a crear una nueva conexion desde esta habitación. Introduce el alias de la habitación con la que quieres conectarla.")
        self.current_process_function = self.process_room_alias

    def process_room_alias(self, message):
        if not message:
            self.session.send_to_client("Prueba otra vez.")
        elif entities.Room.objects(alias=message):
                self.other_room = entities.Room.objects(alias=message).first()
                self.session.send_to_client("¿Cómo quieres llamar a la salida desde aquí? Puedes dejarlo en blanco para un nombre autogenerado.")
                self.current_process_function = self.process_here_exit_name
        else:
            self.session.send_to_client("No hay ninguna sala con ese alias. Prueba otra vez.")

    def process_here_exit_name(self, message):
        if not message:
            message = "camino a {}".format(self.other_room.name)
        
        if message in self.session.user.room.exits.keys():
            self.session.send_to_client('Ya hay una salida con el nombre "{}". Prueba con otro.'.format(message))
        else:
            self.exit_from_here = message
            self.session.send_to_client("¿Cómo quieres llamar a la salida desde la otra habitación? Puedes dejarlo en blanco para un nombre autogenerado.")
            self.current_process_function = self.process_there_exit_name

    def process_there_exit_name(self, message):
        if not message:
            message = "camino a {}".format(self.session.user.room.name)
        
        if message in self.other_room.exits.keys():
            self.session.send_to_client('Ya hay una salida con el nombre "{}". Prueba con otro.'.format(message))
        else:
            self.exit_from_there = message

            self.session.user.room.connect(other_room=self.other_room, exit_name=self.exit_from_here)
            self.other_room.connect(other_room=self.session.user.room, exit_name=self.exit_from_there)

            self.session.send_to_client("Salas conectadas")
            self.session.send_to_others_in_room("Los ojos de {} se ponen en blanco un momento. Una nueva salida aparece en la habitación.".format(self.session.user.name))
            self.finish_interaction()