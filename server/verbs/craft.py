from .verb import Verb
import entities
import util

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
        if util.valid_item_or_exit_name(self.session, message):
            self.new_item_name = message
            self.session.send_to_client("Ahora introduce una descripción para tu nuevo objeto, para que todo el mundo sepa cómo es.")
            self.current_process_function = self.process_item_description
            

    def process_item_description(self, message):
        self.new_item_description = message
        self.session.send_to_client('¿Cuál es la visibilidad del objeto? Escribe:\n  "visible" si nombraste el objeto en la descripción de la sala.\n  "listado" para que se nombre automáticamente al mirar la sala.\n  "oculto" para que los jugadores tengan que encontrarlo por otros medios.\n  "tomable" para que los jugadores puedan coger el objeto y llevarlo consigo. Será listado igual que un verbo listado, y no deberías nombrarlo en la descripción de la sala.')
        self.process = self.process_visibility

    def process_visibility(self, message):
        if message.lower() in ['visible', 'v', 'vi']:
            self.new_item_visibility = 'obvious'
        elif message.lower() in ['listado', 'l', 'li']:
            self.new_item_visibility = 'listed'
        elif message.lower() in ['oculto', 'o', 'oc']:
            self.new_item_visibility = 'hidden'
        elif message.lower() in ['tomable', 't', 'to']:
            # the name of a takable item should be unique across al other items
            if util.valid_takable_item_name(self.session, self.new_item_name):
                self.new_item_visibility = 'takable'
            else:
                self.session.send_to_client("Tendrás que empezar de nuevo.")
                self.finish_interaction()
                return
        else:
            self.session.send_to_client('No te entiendo. Responde "visible", "listado", "oculto" o "tomable.')
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