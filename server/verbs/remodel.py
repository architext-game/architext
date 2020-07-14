from .verb import Verb

class Remodel(Verb):
    command = 'reformar'

    def __init__(self, session):
        super().__init__(session)
        self.option_number = None
        self.current_process_function = self.process_first_message

    def process(self, message):
        self.current_process_function(message)

    def process_first_message(self, message):
        message =  "Vas a editar la habitación en la que te encuentras ({}).\n\rIntroduce el número correspondiente a la propiedad que quieres modificar.\n\r".format(self.session.user.room.name)
        properties = ['0 - Nombre', '1 - Descripción'] + ['{} - Salida a {}.'.format(number+2, other_room.name) for number, other_room in enumerate(self.session.user.room.exits.values())]
        properties_string = "\n\r".join(properties)
        message = message + properties_string 
        self.session.send_to_client(message)
        self.current_process_function = self.process_reform_option

    def process_reform_option(self, message):
        try:
            message = int(message)
        except:
            pass
        max_number = 1 + len(self.session.user.room.exits)
        if 0 <= message <= max_number:
            self.option_number = message
            self.session.send_to_client('Ahora introduce el nuevo valor para esa propiedad.')
            self.current_process_function = self.process_reform_value
        else:
            self.session.send_to_client("Introduce el número correspondiente a una de las opciones.")
        
    def process_reform_value(self, message): 
        option = self.option_number
        if message:
            if option == 0:
                self.session.user.room.name = message
            elif option == 1:
                self.session.user.room.description = message
            else:
                exit_number = option - 2
                exit = list(self.session.user.room.exits.keys())[exit_number]
                room = self.session.user.room.exits.pop(exit)
                self.session.user.room.exits[message] = room
            self.session.user.room.save()
            self.session.send_to_client('Reforma completada con éxito.')
            self.finished = True
        else:
            self.session.send_to_client('Debes introducir el nuevo valor.')