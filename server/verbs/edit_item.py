from .verb import Verb
import entities

class EditItem(Verb):
    """This verb allows users to edit properties of an item or exit that is in their current room"""

    command = 'editar '

    def __init__(self, session):
        super().__init__(session)
        self.option_number = None
        self.item_to_edit = None
        self.exit_to_edit = None
        self.current_process_function = self.start_editing

    def process(self, message):
        self.current_process_function(message)

    def start_editing(self, message):
        current_room = self.session.user.room
        message = message[len(self.command):]

        if message in [item.name for item in current_room.items]:
            for item in self.session.user.room.items:
                if item.name == message:
                    self.item_to_edit = item
                    break
            self.session.send_to_client("Introduce el número correspondiente al atributo a eidtar.\n  [0] Nombre\n  [1] Descripción\n  [2] Visibilidad")
            self.current_process_function = self.process_item_edit_option_number

        elif message in [exit.name for exit in current_room.exits]:
            for exit in self.session.user.room.exits:
                if exit.name == message:
                    self.exit_to_edit = exit
                    break
            self.session.send_to_client("Introduce el número correspondiente al atributo a eidtar.\n  [0] Nombre\n  [1] Descripción\n  [2] Visibilidad\n  [3] Destino")
            self.current_process_function = self.process_exit_edit_option_number

        else:
            self.session.send_to_client("No encuentras ningún objeto ni salida con ese nombre.")
            self.finish_interaction()

    def process_item_edit_option_number(self, message):
        try:
            message = int(message)
        except:
            self.session.send_to_client('Debes introducir un número.')
            return

        # max_number = 2
        if 0 <= message <= 1:
            self.option_number = message
            self.session.send_to_client('Ahora introduce el nuevo valor para esa propiedad.')
            self.current_process_function = self.process_reform_value
        elif message == 2:
            self.option_number = message
            self.session.send_to_client('¿Qué visibilidad prefieres?. Escribe:\n  "visible" si nombraste el objeto en la descripción de la sala.\n  "listado" para que se nombre automáticamente al mirar la sala.\n  "oculto" para que los jugadores tengan que encontrarlo por otros medios.')
            self.current_process_function = self.process_reform_value
        else:
            self.session.send_to_client("Introduce el número correspondiente a una de las opciones.")

    def process_exit_edit_option_number(self, message):
        try:
            message = int(message)
        except:
            self.session.send_to_client('Debes introducir un número.')
            return

        if message == 3:
            self.option_number = message
            self.session.send_to_client('Introduce el alias de la sala a la que quieres que lleve esta salida. (Puedes encontrarlo escribiendo "info" allí).')
            self.current_process_function = self.process_reform_value
        else:
            self.process_item_edit_option_number(message)
    
    def process_reform_value(self, message):
        object_to_edit = self.item_to_edit if self.item_to_edit else self.exit_to_edit
        
        if message:
            if self.option_number == 0:  # edit name
                object_to_edit.name = message
            elif self.option_number == 1:  # edit description
                object_to_edit.description = message
            elif self.option_number == 2:  # edit visibility
                if message.lower() in ['visible', 'v', 'vi']:
                    object_to_edit.visible = 'obvious'
                elif message.lower() in ['listado', 'l', 'li']:
                    object_to_edit.visible = 'listed'
                elif message.lower() in ['oculto', 'o', 'oc']:
                    object_to_edit.visible = 'hidden'
                else:
                    self.session.send_to_client('No te entiendo. Responde "visible", "listado" u "oculto".')
                    return
            elif self.option_number == 3:  # edit exit's destination
                if entities.Room.objects(alias=message):
                    object_to_edit.destination = entities.Room.objects(alias=message).first()
                else:
                    self.session.send_to_client('No existe una sala con ese alias. Terminando edición.')
                    self.finish_interaction()
                    return
            object_to_edit.save()
            self.session.send_to_client('Hecho.')
            self.finish_interaction()
        else:
            self.session.send_to_client('Debes introducir el nuevo valor')