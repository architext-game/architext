from .verb import Verb
from .look import Look 

class Go(Verb):
    command = 'ir '

    def process(self, message):
        command_length = len(self.command)
        partial_exit_name = message[command_length:]
        if partial_exit_name in self.session.user.room.exits:
                self.go(exit)
        elif [partial_exit_name in room_exit for room_exit in self.session.user.room.exits.keys()].count(True) == 1:
                for room_exit in self.session.user.room.exits.keys():
                    if partial_exit_name in room_exit:
                        exit_name = room_exit
                self.go(exit_name)
        elif [exit in room_exit for room_exit in self.session.user.room.exits.keys()].count(True) > 1:
            self.session.send_to_client('Hay más de una salida con ese nombre. Sé más específico.')
        else:
            self.session.send_to_client("No puedes encontrar esa salida.")

        self.finished = True

    def go(self, exit):
        origin_room = self.session.user.room
        self.session.send_to_others_in_room("{} se marcha por {}.".format(self.session.user.name, exit))
        self.session.user.move(exit)
        there_exit = [exit for exit, room in self.session.user.room.exits.items() if room == origin_room][0]
        self.session.send_to_others_in_room("{} llega desde {}.".format(self.session.user.name, there_exit))
        Look(self.session).show_current_room()
