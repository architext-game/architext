from . import verb
from .. import entities
from .. import util

class Craft(verb.Verb):
    """This verb allows users to create items that are placed in their current room"""

    command = 'fabricar'
    permissions = verb.PRIVILEGED

    def __init__(self, session):
        super().__init__(session)
        self.new_item = entities.Item(room=self.session.user.room, save_on_creation=False)
        self.current_process_function = self.process_first_message

    def process(self, message):
        self.current_process_function(message)

    def process_first_message(self, message):
        self.session.send_to_client("Comienzas a fabricar un objeto. ¿Cómo quieres llamarlo?")
        self.current_process_function = self.process_item_name

    def process_item_name(self, message):
        self.new_item.name = message
        try:
            self.new_item.ensure_i_am_valid()
        except entities.EmptyName:
            self.session.send_to_client("El nombre no puede estar vacío. Prueba con otro.")
        except entities.WrongNameFormat:
            self.session.send_to_client("El nombre no puede acabar con # y un número. Prueba con otro.")
        except entities.RoomNameClash:
            self.session.send_to_client("Ya hay un objeto o salida con ese nombre en esta sala. Prueba con otro.")
        except entities.TakableItemNameClash:
            self.session.send_to_client("Hay en el mundo un objeto tomable con ese nombre. Los objetos tomables deben tener un nombre único en todo el mundo, así que prueba a poner otro.")
        else:
            self.session.send_to_client("Ahora introduce una descripción para tu nuevo objeto, para que todo el mundo sepa cómo es.")
            self.current_process_function = self.process_item_description
 
    def process_item_description(self, message):
        self.new_item.description = message
        self.session.send_to_client('¿Cuál es la visibilidad del objeto? Escribe:\n  "visible" si nombraste el objeto en la descripción de la sala.\n  "listado" para que se nombre automáticamente al mirar la sala.\n  "oculto" para que los jugadores tengan que encontrarlo por otros medios.\n  "cogible" para que los jugadores puedan coger el objeto y llevarlo consigo. Será listado igual que un verbo listado, y no deberías nombrarlo en la descripción de la sala.')
        self.process = self.process_visibility

    def process_visibility(self, message):
        if message.lower() in ['visible', 'v', 'vi']:
            self.new_item.visible = 'obvious'
        elif message.lower() in ['listado', 'l', 'li']:
            self.new_item.visible = 'listed'
        elif message.lower() in ['oculto', 'o', 'oc']:
            self.new_item.visible = 'hidden'
        elif message.lower() in ['cogible', 'c', 'co']:
            self.new_item.visible = 'takable'
        else:
            self.session.send_to_client('No te entiendo. Responde "visible", "listado", "oculto" o "cogible.')
            return

        try:
            self.new_item.save()
        except entities.NameNotGloballyUnique:
            self.session.send_to_client("Ya hay en el mundo un objeto o una salida con este nombre. Los objetos cogibles deben tener un nombre totalmente único. Tendrás que empezar a crearlo de nuevo.")
        else:
            self.new_item.put_in_room(self.session.user.room)
            self.session.send_to_client("¡Objeto creado!")
            if not self.session.user.master_mode:
                self.session.send_to_others_in_room("{} acaba de crear algo aquí.".format(self.session.user.name))
        self.finish_interaction()