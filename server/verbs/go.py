from .verb import Verb
from .look import Look 
import util

class Go(Verb):
    """Allows the user to travel between rooms, using their exits."""

    command = 'ir '

    def process(self, message):
        command_length = len(self.command)
        partial_exit_name = message[command_length:]
        available_exits = [exit.name for exit in self.session.user.room.exits]
        possible_meanings = util.possible_meanings(partial_exit_name, available_exits)
        if len(possible_meanings) == 1:
            selected_exit_name = possible_meanings[0]
            selected_exit = next(filter(lambda e: e.name==selected_exit_name, self.session.user.room.exits))
            self.go(selected_exit)
        elif len(possible_meanings) > 1:
            self.session.send_to_client('Hay más de una salida con ese nombre. Sé más específico.')
        elif len(possible_meanings) == 0:
            self.session.send_to_client("No puedes encontrar esa salida.")

        self.finish_interaction()

    def go(self, selected_exit):
        if not self.session.user.master_mode:
            if not selected_exit.is_open:
                self.session.send_to_client("Esa salida está cerrada.")
                return

        origin_room = self.session.user.room
        self.session.user.move(selected_exit.name)
        there_exit = [exit.name for exit in self.session.user.room.exits if exit.destination == origin_room and not exit.hidden()]

        if not self.session.user.master_mode:
            if not selected_exit.hidden():
                self.session.send_to_others_in_room("{} se marcha por {}.".format(self.session.user.name, selected_exit.name))
            else:
                self.session.send_to_others_in_room("{} se marcha hacia algún lugar.".format(self.session.user.name))
            if there_exit:
                self.session.send_to_others_in_room("{} llega desde {}.".format(self.session.user.name, there_exit[0]))
            else:
                self.session.send_to_others_in_room("{} llega desde algún lugar.".format(self.session.user.name))

        Look(self.session).show_current_room()
