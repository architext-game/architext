# Issue: directly changes room values, and calls save() method.

from . import verb

class Remodel(verb.Verb):
    """Lets players edit every aspect of a room"""

    command = 'reformar'
    permissions = verb.PRIVILEGED

    def __init__(self, session):
        super().__init__(session)
        self.option_number = None
        self.current_process_function = self.process_first_message

    def process(self, message):
        if message == '/':
            self.session.send_to_client("Reforma cancelada.")
            self.finish_interaction()
        else:
            self.current_process_function(message)

    def process_first_message(self, message):
        message = f"Reformando {self.session.user.room.name}\n{chr(9472)*(12+len(self.session.user.room.name))}\n{chr(10060)} Para cancelar, introduce '/' en cualquier momento.\n\n¿Qué quieres cambiar? (introduce el número correspondiente)\n"
        properties = [' 0 - Nombre', ' 1 - Descripción']
        properties_string = "\n".join(properties)
        message = message + properties_string 
        self.session.send_to_client(message)
        self.current_process_function = self.process_reform_option

    def process_reform_option(self, message):
        try:
            message = int(message)
        except:
            self.session.send_to_client('Debes introducir un número.')
            return

        max_number = 1
        if 0 <= message <= max_number:
            self.option_number = message
            self.session.send_to_client('Introduce el nuevo valor')
            self.current_process_function = self.process_reform_value
        else:
            self.session.send_to_client('Introduce el número correspondiente a una de las opciones o "/" para cancelar')
        
    def process_reform_value(self, message): 
        option = self.option_number
        if message:
            if option == 0:
                self.session.user.room.name = message
            elif option == 1:
                self.session.user.room.description = message
            self.session.user.room.save()
            self.session.send_to_client('Reforma completada.')
            self.finish_interaction()
        else:
            self.session.send_to_client('Debes introducir el nuevo valor.')