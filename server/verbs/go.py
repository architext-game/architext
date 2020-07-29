from .verb import Verb
from .look import Look 
import util

class Go(Verb):
    """Allows the user to travel between rooms, using their exits."""

    command = 'ir '

    def process(self, message):
        command_length = len(self.command)
        partial_exit_name = message[command_length:]
        available_exits = list(self.session.user.room.exits.keys())
        possible_meanings = util.possible_meanings(partial_exit_name, available_exits)
        if len(possible_meanings) == 1:
            selected_exit = possible_meanings[0]
            self.go(selected_exit)
        elif len(possible_meanings) > 1:
            self.session.send_to_client('Hay más de una salida con ese nombre. Sé más específico.')
        elif len(possible_meanings) == 0:
            self.session.send_to_client("No puedes encontrar esa salida.")

        self.finish_interaction()

    def go(self, exit):
        origin_room = self.session.user.room
        self.session.send_to_others_in_room("{} se marcha por {}.".format(self.session.user.name, exit))
        self.session.user.move(exit)
        there_exit = [exit for exit, room in self.session.user.room.exits.items() if room == origin_room][0]
        self.session.send_to_others_in_room("{} llega desde {}.".format(self.session.user.name, there_exit))
        Look(self.session).show_current_room()
