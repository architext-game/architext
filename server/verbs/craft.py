from .verb import Verb
import entities

class Craft(Verb):
    """This verb allows users to create items that are placed in their current room"""

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
        self.session.send_to_client("Comienzas a fabricar un objeto. ¿Cómo quieres llamarlo?")
        self.current_process_function = self.process_item_name

    def process_item_name(self, message):
        if not message:
            self.session.send_to_client("Tienes que poner un nombre a tu objeto. Prueba otra vez.")
        elif message in [item.name for item in self.session.user.room.items]:
            self.session.send_to_client("Ese objeto ya está en esta sala. Prueba a ponerle otro nombre")
        elif message in [exit.name for exit in self.session.user.room.exits]:
            self.session.send_to_client("Ya hay una salida con el nombre que quieres poner al objeto. Prueba con otro.")
        else:
            self.new_item_name = message
            self.session.send_to_client("Ahora introduce una descripción para tu nuevo objeto, para que todo el mundo sepa cómo es.")
            self.current_process_function = self.process_item_description

    def process_item_description(self, message):
        self.new_item_description = message
        self.session.send_to_client('¿Cuál es la visibilidad del objeto? Escribe:\n  "visible" si nombraste el objeto en la descripción de la sala.\n  "listado" para que se nombre automáticamente al mirar la sala.\n  "oculto" para que los jugadores tengan que encontrarlo por otros medios.')
        self.process = self.process_visibility

    def process_visibility(self, message):
        if message.lower() in ['visible', 'v', 'vi']:
            self.new_item_visibility = 'obvious'
        elif message.lower() in ['listado', 'l', 'li']:
            self.new_item_visibility = 'listed'
        elif message.lower() in ['oculto', 'o', 'oc']:
            self.new_item_visibility = 'hidden'
        else:
            self.session.send_to_client('No te entiendo. Responde "visible", "listado" u "oculto".')
            return

        new_item = entities.Item(
            name=self.new_item_name, 
            description=self.new_item_description, 
            visible=self.new_item_visibility
        )
        self.session.user.room.add_item(new_item)
        self.session.send_to_client("¡Objeto creado!")
        if not self.session.user.master_mode:
            self.session.send_to_others_in_room("{} acaba de crear algo aquí.".format(self.session.user.name))
        self.finish_interaction()