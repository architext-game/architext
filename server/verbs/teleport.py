from .verb import Verb
from .look import Look 
import util
import entities

class Teleport(Verb):
    command = 'tp '

    def process(self, message):
        command_length = len(self.command)
        room_alias = message[command_length:]
        
        query = entities.Room.objects(alias=room_alias)
        if len(query) == 1:
            self.teleport(query.first())
        elif len(query) > 1:
            self.session.send_to_client('Hay más de una sala con ese alias. Esto no debería pasar.')
        elif len(query) == 0:
            self.session.send_to_client("NO hay ninguna sala con ese alias.")

        self.finished = True

    def go(self, exit):
        origin_room = self.session.user.room
        self.session.send_to_others_in_room("{} se marcha por {}.".format(self.session.user.name, exit))
        self.session.user.move(exit)
        there_exit = [exit for exit, room in self.session.user.room.exits.items() if room == origin_room][0]
        self.session.send_to_others_in_room("{} llega desde {}.".format(self.session.user.name, there_exit))
        Look(self.session).show_current_room()

    def teleport(self, room):
        self.session.user.teleport(room)
        Look(self.session).show_current_room()
