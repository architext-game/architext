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
            selected_exit = possible_meanings[0]
            self.go(selected_exit)
        elif len(possible_meanings) > 1:
            self.session.send_to_client('Hay más de una salida con ese nombre. Sé más específico.')
        elif len(possible_meanings) == 0:
            self.session.send_to_client("No puedes encontrar esa salida.")

        self.finish_interaction()

    def go(self, exit_name):
        origin_room = self.session.user.room
        self.session.send_to_others_in_room("{} se marcha por {}.".format(self.session.user.name, exit_name))
        self.session.user.move(exit_name)
        try:
            there_exit = [exit.name for exit in self.session.user.room.exits if exit.destination == origin_room][0]
            self.session.send_to_others_in_room("{} llega desde {}.".format(self.session.user.name, there_exit))
        except:
            self.session.send_to_others_in_room("{} llega desde algún lugar.".format(self.session.user.name))
        Look(self.session).show_current_room()
