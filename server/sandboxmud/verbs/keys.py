from . import verb
from .. import util

class MasterClose(verb.Verb):
    command = "cierradirector "
    permissions = verb.PRIVILEGED

    def process(self, message):
        command_length = len(self.command)
        exit_name = message[command_length:]
        exit_to_close = next(filter(lambda e: e.name==exit_name, self.session.user.room.exits), None)
        if exit_to_close is not None:
            exit_to_close.close()
            self.session.send_to_client("Cerrada.")
        else:
            self.session.send_to_client("No encuentras esa salida")

        self.finish_interaction()


class MasterOpen(verb.Verb):
    command = "abredirector "
    permissions = verb.PRIVILEGED

    def process(self, message):
        command_length = len(self.command)
        exit_name = message[command_length:]
        exit_to_open = next(filter(lambda e: e.name==exit_name, self.session.user.room.exits), None)
        if exit_to_open is not None:
            exit_to_open.open()
            self.session.send_to_client("Abierta.")
        else:
            self.session.send_to_client("No encuentras esa salida")

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
        self.exit_to_assign = next(filter(lambda e: e.name==exit_name, self.session.user.room.exits), None)
        if self.exit_to_assign is not None:
            self.current_process_function = self.process_item_name
            self.session.send_to_client("¿Cómo se llama el objeto que debe abrir esta salida? ('/' para cancelar)")
        else:
            self.session.send_to_client("No encuentras esa salida.")
            self.finish_interaction()

    def process_item_name(self, message):
        self.exit_to_assign.add_key(message)
        self.session.send_to_client("Llave añadida.")
        self.finish_interaction()


class Open(verb.Verb):
    command = "abrir "

    def process(self, message):
        command_length = len(self.command)
        partial_exit_name = message[command_length:]
        available_exits = [exit.name for exit in self.session.user.room.exits]
        possible_meanings = util.possible_meanings(partial_exit_name, available_exits)
        if len(possible_meanings) == 1:
            selected_exit_name = possible_meanings[0]
            selected_exit = next(filter(lambda e: e.name==selected_exit_name, self.session.user.room.exits))
            self.open(selected_exit)
        elif len(possible_meanings) > 1:
            self.session.send_to_client('Hay más de una salida con ese nombre. Sé más específico.')
        elif len(possible_meanings) == 0:
            self.session.send_to_client("No puedes encontrar esa salida.")

        self.finish_interaction()

    def open(self, exit_to_open):
        if(exit_to_open.is_open):
            self.session.send_to_client("Esa salida ya está abierta.")
            return

        for item in self.session.user.get_current_world_inventory().items:
            if item.name in exit_to_open.key_names:
                exit_to_open.open()
                self.session.send_to_client("Abres la salida con {}.".format(item.name))
                return

        self.session.send_to_client("No puedes abrirla.")


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
        self.chosen_exit = next(filter(lambda e: e.name==exit_name, self.session.user.room.exits), None)
        if self.chosen_exit is not None:
            if len(self.chosen_exit.key_names) > 0:
                out_message = "¿Qué llave quieres eliminar?"
                for index, key in enumerate(self.chosen_exit.key_names):
                    out_message += f"\n   {index}. {key}"
                out_message += "\n* para eliminar todas las llaves asignadas."
                out_message += "\n/ para cancelar."
                self.session.send_to_client(out_message)
                self.current_process_function = self.process_key_index
            else:
                self.session.send_to_client("Esta salida no tiene ninguna llave asignada.")
                self.finish_interaction()
        else:
            self.session.send_to_client("No encuentras esa salida.")
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


        



            