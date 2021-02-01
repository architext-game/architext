from .verb import Verb
from .. import util

class Build(Verb):
    """This verb allows the user to create a new room connected to his current location.
    All the user need to know is the command he should write to start creation. That
    command will start a text wizard that drives him across the creation process.
    """
    command = 'construir'

    def __init__(self, session):
        super().__init__(session)
        self.new_room_name = None
        self.new_room_description = None
        self.exit_from_here = None
        self.exit_from_there = None
        self.current_process_function = self.process_first_message

    def process(self, message):
        self.current_process_function(message)

    def process_first_message(self, message):
        self.session.send_to_client("Comienzas a construir una habitación. ¿Cómo quieres llamarla?")
        self.current_process_function = self.process_room_name

    def process_room_name(self, message):
        if not message:
            self.session.send_to_client("Tienes que poner un nombre a tu habitación. Prueba otra vez.")
        else:
            self.new_room_name = message
            self.session.send_to_client("Ahora introduce una descripción para tu nueva sala, para que todo el mundo sepa cómo es.")
            self.current_process_function = self.process_room_description

    def process_room_description(self, message):
        self.new_room_description = message
        current_room = self.session.user.room.name
        new_room = self.new_room_name
        self.session.send_to_client("Cómo quieres llamar a la salida desde {} a {}? Si no se te ocurre nada, puedes dejarlo en blanco.".format(current_room, new_room))
        self.current_process_function = self.process_here_exit_name

    def process_here_exit_name(self, message):
        if not message:
            message = "a {}".format(self.new_room_name)
            while(not util.valid_item_or_exit_name(self.session, message)):
                message = 'directo ' + message

        if not util.valid_item_or_exit_name(self.session, message):
            self.session.send_to_client('Introduce otro nombre.'.format(message))
        else:
            self.exit_from_here = message
        
            current_room = self.session.user.room.name
            new_room = self.new_room_name
            self.session.send_to_client("Cómo quieres llamar a la salida desde {} a {}? Si no se te ocurre nada, puedes dejarlo en blanco.".format(new_room, current_room))
            self.current_process_function = self.process_there_exit_name

    def process_there_exit_name(self, message):
        if not message:
            default_message = "a {}".format(self.session.user.room.name)
            while(not util.name_globaly_free(self.session, default_message)):
                default_message = 'directo ' + default_message
            self.exit_from_there =  default_message
        else:
            if not util.name_globaly_free(self.session, message):
                session.send_to_client("En este mundo hay un objeto cogible con ese nombre. Debes elegir otro.")
                return
            self.exit_from_there = message

        self.session.user.room.create_adjacent_room(
            there_name = self.new_room_name,
            there_description = self.new_room_description,
            exit_from_here = self.exit_from_here,
            exit_from_there = self.exit_from_there
        )
        self.session.send_to_client("¡Enhorabuena! Tu nueva habitación está lista.")
        if not self.session.user.master_mode:
            self.session.send_to_others_in_room("Los ojos de {} se ponen en blanco un momento. Una nueva salida aparece en la habitación.".format(self.session.user.name))
        self.finish_interaction()

    def make_exit_name_valid(self, exit_name):
        is_valid = False
        while not is_valid:
            try:
                entities.Exit.check_exit_name(exit_name, self.session.user.room)
                is_valid = True
            except (ItemNameClash, ExitNameClash, TakableItemNameClash):
                exit_name = 'directo ' + exit_name
        return exit_name