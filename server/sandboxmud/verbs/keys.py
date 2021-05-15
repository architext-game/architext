from . import verb
from .. import util

class MasterClose(verb.Verb):
    command = "cierradirector "
    permissions = verb.PRIVILEGED

    def process(self, message):
        command_length = len(self.command)
        exit_name = message[command_length:]
        exit_to_close = util.name_to_entity(self.session, exit_name, substr_match=["room_exits"])

        if exit_to_close == "many":
            self.session.send_to_client("Hay varias salidas con un nombre similar a ese. Sé más específico.")
        elif exit_to_close is None:
            self.session.send_to_client("No encuentras esa salida")
        else:
            exit_to_close.close()
            self.session.send_to_client(f'Salida "{exit_to_close.name}" cerrada.')

        self.finish_interaction()


class MasterOpen(verb.Verb):
    command = "abredirector "
    permissions = verb.PRIVILEGED

    def process(self, message):
        command_length = len(self.command)
        exit_name = message[command_length:]
        exit_to_open = util.name_to_entity(self.session, exit_name, substr_match=["room_exits"])

        if exit_to_open == "many":
            self.session.send_to_client("Hay varias salidas con un nombre similar a ese. Sé más específico.")
        elif exit_to_open is None:
            self.session.send_to_client("No encuentras esa salida")
        else:
            exit_to_open.open()
            self.session.send_to_client(f'Salida "{exit_to_open.name}" abierta.')

        self.finish_interaction()


class AssignKey(verb.Verb):
    command = "asignarllave "
    permissions = verb.PRIVILEGED

    def __init__(self, session):
        super().__init__(session)
        self.exit_to_assign = None
        self.current_process_function = self.process_exit_name

    def process(self, message):
        if message == '/':
            self.session.send_to_client("Asignación de llave cancelada.")
            self.finish_interaction()
        else:
            self.current_process_function(message)

    def process_exit_name(self, message):
        command_length = len(self.command)
        exit_name = message[command_length:]
        self.exit_to_assign = util.name_to_entity(self.session, exit_name, substr_match=["room_exits"])

        if self.exit_to_assign == "many":
            self.session.send_to_client("Hay varias salidas con un nombre similar a ese. Sé más específico.")
            self.finish_interaction()
        elif self.exit_to_assign is None:
            self.session.send_to_client("No encuentras esa salida")
            self.finish_interaction()
        else:
            self.current_process_function = self.process_item_name
            self.session.send_to_client(f'¿Cómo se llama el objeto que debe abrir "{self.exit_to_assign.name}"? ("/" para cancelar)')

    def process_item_name(self, message):
        self.exit_to_assign.add_key(message)
        self.session.send_to_client("Llave añadida.")
        self.finish_interaction()


class Open(verb.Verb):
    command = "abrir "

    def process(self, message):
        command_length = len(self.command)
        partial_exit_name = message[command_length:]
        selected_exit = util.name_to_entity(self.session, partial_exit_name, substr_match=["room_exits"])

        if selected_exit == "many":
            self.session.send_to_client("Hay varias salidas con un nombre similar a ese. Sé más específico.")
        elif selected_exit is None:
            self.session.send_to_client("No encuentras esa salida")
        else:
            self.open(selected_exit)

        self.finish_interaction()

    def open(self, exit_to_open):
        if(exit_to_open.is_open):
            self.session.send_to_client(f'La salida "{exit_to_open.name}" ya está abierta.')
            return

        for item in self.session.user.get_current_world_inventory().items:
            if item.name in exit_to_open.key_names:
                exit_to_open.open()
                self.session.send_to_client(f'Abres la salida "{exit_to_open.name}" con {item.name}.')
                return

        self.session.send_to_client(f'No puedes abrir "{exit_to_open.name}".')


class DeleteKey(verb.Verb):
    command = "eliminarllave "
    permissions = verb.PRIVILEGED

    def __init__(self, session):
        super().__init__(session)
        self.chosen_exit = None
        self.current_process_function = self.process_exit_name

    def process(self, message):
        if message == '/':
            self.session.send_to_client("Eliminación de llave cancelada.")
            self.finish_interaction()
        else:
            self.current_process_function(message)

    def process_exit_name(self, message):
        command_length = len(self.command)
        exit_name = message[command_length:]
        self.chosen_exit = util.name_to_entity(self.session, partial_exit_name, substr_match=["room_exits"])

        if self.chosen_exit == "many":
            self.session.send_to_client("Hay varias salidas con un nombre similar a ese. Sé más específico.")
            self.finish_interaction()
        elif self.chosen_exit is None:
            self.session.send_to_client("No encuentras esa salida")
            self.finish_interaction()
        else:
            if len(self.chosen_exit.key_names) > 0:
                out_message = f'Salida: {self.chosen_exit.name}'
                out_message += "\n¿Qué llave quieres eliminar?"
                for index, key in enumerate(self.chosen_exit.key_names):
                    out_message += f"\n   {index}. {key}"
                out_message += "\n* para eliminar todas las llaves asignadas."
                out_message += "\n/ para cancelar."
                self.session.send_to_client(out_message)
                self.current_process_function = self.process_key_index
            else:
                self.session.send_to_client(f'La salida "{self.chosen_exit.name}" no tiene ninguna llave asignada.')
                self.finish_interaction()

    def process_key_index(self, message):
        if message == '*':
            keys_to_delete = self.chosen_exit.key_names.copy()
        else:
            try:
                index = int(message)
                if index < 0:
                    raise ValueError
            except ValueError:
                self.session.send_to_client("Introduce un número")
                return
            try:
                keys_to_delete = [ self.chosen_exit.key_names[index] ]
            except IndexError:
                self.session.send_to_client("Introduce el número correspondiente a una de las llaves")
                return

        for key_to_delete in keys_to_delete:
            self.chosen_exit.remove_key(key_to_delete)

        self.session.send_to_client('Llave/s eliminada/s.')
        self.finish_interaction()


        



            