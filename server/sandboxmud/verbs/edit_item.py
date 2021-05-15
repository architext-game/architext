from . import verb
from .. import util
from .. import entities
import textwrap

class EditItem(verb.Verb):
    """This verb allows users to edit properties of an item or exit that is in their current room"""

    command = 'editar '
    permissions = verb.PRIVILEGED

    def __init__(self, session):
        super().__init__(session)
        self.option_number = None
        self.item_to_edit = None
        self.exit_to_edit = None
        self.current_process_function = self.start_editing

    def process(self, message):
        if message == '/':
            self.session.send_to_client("Edición cancelada.")
            self.finish_interaction()
        else:
            self.current_process_function(message)

    def start_editing(self, message):
        current_room = self.session.user.room
        message = message[len(self.command):]
        saved_items = entities.Item.objects(saved_in=self.session.user.room.world_state)

        selected_entity = util.name_to_entity(self.session, message, loose_match=["saved_items"], substr_match=["room_items", "inventory", "room_exits"])

        if selected_entity == "many":
            self.session.send_to_client('Hay más de un objeto o salida con un nombre similar a ese. Se más específico.')
            self.finish_interaction()
            return
        elif selected_entity is None:
            self.session.send_to_client('No hay ningún objeto o salida con ese nombre en esta sala, ni objeto guardado con ese identificador.')
            self.finish_interaction()
            return

        if isinstance(selected_entity, entities.Item):
            self.item_to_edit = selected_entity

            if self.item_to_edit.is_saved():
                header = textwrap.dedent(f"""
                    Editando {self.item_to_edit.item_id} (objeto guardado)
                    {chr(9472)*(10+len(self.item_to_edit.item_id))}"""
                )
            else:
                header = textwrap.dedent(f"""
                    Editando {self.item_to_edit.name} (objeto en la sala)
                    {chr(9472)*(10+len(self.item_to_edit.name))}"""
                )

            out_message = textwrap.dedent(f"""
                {header}
                
                {chr(10060)} Para cancelar, introduce '/' en cualquier momento.
                
                ¿Qué quieres cambiar? (introduce el número correspondiente)
                    1 - Descripción
                    0 - Nombre
                    2 - Visibilidad"""
            )
            self.session.send_to_client(out_message)
            self.next_process_function = self.process_item_edit_option_number

        elif isinstance(selected_entity, entities.Exit):
            self.exit_to_edit = selected_entity

            out_message = textwrap.dedent(f"""
                Editando {self.exit_to_edit.name} (salida)
                {chr(9472)*(10+len(self.exit_to_edit.name))}
                {chr(10060)} Para cancelar, introduce '/' en cualquier momento.
                
                ¿Qué quieres cambiar? (introduce el número correspondiente)
                    0 - Nombre
                    1 - Descripción 
                    2 - Visibilidad
                    3 - Destino"""
            )

            self.session.send_to_client(out_message)
            self.current_process_function = self.process_exit_edit_option_number

        else:
            raise ValueError(f"Expected Room or Exit, {type(selected_entity)} found")


    def process_item_edit_option_number(self, message):
        try:
            message = int(message)
        except ValueError:
            self.session.send_to_client('Debes introducir un número.')
            return

        # max_number = 2
        if 0 <= message <= 1:
            self.option_number = message
            self.session.send_to_client('Introduce el nuevo valor')
            self.current_process_function = self.process_reform_value
        elif message == 2:
            self.option_number = message
            self.session.send_to_client('¿Qué visibilidad prefieres? Escribe:\n  "visible" si nombraste el objeto en la descripción de la sala.\n  "listado" para que se nombre automáticamente al mirar la sala.\n  "oculto" para que los jugadores tengan que encontrarlo por otros medios.\n  "cogible" para que los jugadores puedan coger el objeto y llevarlo consigo. Será listado igual que un verbo listado, y no deberías nombrarlo en la descripción de la sala.')
            self.current_process_function = self.process_reform_value
        else:
            self.session.send_to_client("Introduce el número correspondiente a una de las opciones.")

    def process_exit_edit_option_number(self, message):
        try:
            message = int(message)
        except ValueError:
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
                try:
                    object_to_edit.ensure_i_am_valid()
                except entities.NameNotGloballyUnique:
                    self.session.send_to_client('Ya hay un objeto con ese nombre en este mundo. El objeto que tratas de editar es cogible, y por eso no puede compartir nombre con ningún otro objeto. Se cancela la edición.')
                    self.finish_interaction()
                    return
                except entities.EmptyName:
                    self.session.send_to_client('No puedes poner un nombre vacío. Se cancela la edición.')
                    self.finish_interaction()
                    return
                except entities.WrongNameFormat:
                    self.session.send_to_client('El nombre no puede terminar con # y un número. Se cancela la edición.')
                    self.finish_interaction()
                    return
                except entities.RoomNameClash:
                    self.session.send_to_client('Ya hay un objeto o salida con ese nombre en esta sala. Se cancela la edición.')
                    self.finish_interaction()
                    return
                except entities.TakableItemNameClash:
                    self.session.send_to_client('Hay un objeto cogible con ese nombre en este mundo. Se cancela la edición.')
                    self.finish_interaction()
                    return
            elif self.option_number == 1:  # edit description
                object_to_edit.description = message
            elif self.option_number == 2:  # edit visibility
                if message.lower() in ['visible', 'v', 'vi']:
                    object_to_edit.visible = 'obvious'
                elif message.lower() in ['listado', 'l', 'li']:
                    object_to_edit.visible = 'listed'
                elif message.lower() in ['oculto', 'o', 'oc']:
                    object_to_edit.visible = 'hidden'
                elif message.lower() in ['cogible', 'c', 'co']:
                    if self.can_change_to_takable(self.item_to_edit):
                        object_to_edit.visible = 'takable'
                    else:
                        self.session.send_to_client("Por lo tanto, no se puede asignar esa visibilidad a tu objeto. Prueba a cambiarle el nombre primero.")
                        self.finish_interaction()
                        return
                else:
                    self.session.send_to_client('No te entiendo. Responde "visible", "listado", "oculto" o "cogible".')
                    return
            elif self.option_number == 3:  # edit exit's destination
                if entities.Room.objects(alias=message):
                    object_to_edit.destination = entities.Room.objects(alias=message).first()
                else:
                    self.session.send_to_client('No existe una sala con ese alias. Terminando edición.')
                    self.finish_interaction()
                    return
            object_to_edit.save()
            self.session.send_to_client('Edición completada.')
            self.finish_interaction()
        else:
            self.session.send_to_client('Debes introducir el nuevo valor')


    def can_change_to_takable(self, item_to_change):
        return entities.Item.name_is_valid(item_to_change.name, self.session.user.room, ignore_item=item_to_change, takable=True)
