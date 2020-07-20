from .verb import Verb
from entities import Item

class Craft(Verb):
    command = 'fabricar'

    def __init__(self, session):
        super().__init__(session)
        self.new_item_name = None
        self.new_item_description = None
        self.new_item_visibility = None
        self.current_process_function = self.process_first_message

    def process(self, message):
        self.current_process_function(message)

    def process_first_message(self, message):
        self.session.send_to_client("Comienzas a frabricar un objeto. ¿Cómo quieres llamarlo?")
        self.current_process_function = self.process_item_name

    def process_item_name(self, message):
        if not message:
            self.session.send_to_client("Tienes que poner un nombre a tu objeto. Prueba otra vez.")
        elif message in [item.name for item in self.session.user.room.items]:
            self.session.send_to_client("Ese objeto ya está en esta sala. Prueba a ponerle otro nombre")
        else:
            self.new_item_name = message
            self.session.send_to_client("Ahora introduce una descripción para tu nuevo objeto, para que todo el mundo sepa cómo es.")
            self.current_process_function = self.process_item_description

    def process_item_description(self, message):
        self.new_item_description = message
        self.session.send_to_client('¿Quieres que tu objeto aparezca en la lista de objetos presentes en la sala? (Responde "si" o "no")')
        self.process = self.process_visibility

    def process_visibility(self, message):
        if message.lower() in ['sí', 'si', 's']:
            self.new_item_visibility = True
        elif message.lower() in ['no', 'n']:
            self.new_item_visibility = False
        else:
            self.session.send_to_client('No te entiendo. Responde "si" o "no".')
            return

        new_item = Item(
            name=self.new_item_name, 
            description=self.new_item_description, 
            visible=self.new_item_visibility
        )
        self.session.user.room.add_item(new_item)
        self.session.send_to_client("¡Objeto creado!")
        self.session.send_to_others_in_room("{} acaba de crear algo aquí.".format(self.session.user.name))
        self.finished = True