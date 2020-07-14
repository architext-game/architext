from .verb import Verb
from entities import User

class Look(Verb):
    command = 'mirar'

    def process(self, message):
        self.show_current_room()
        self.finished = True

    def show_current_room(self):
        self.session.user.room.reload()
        title = self.session.user.room.name
        description = self.session.user.room.description if self.session.user.room.description else "Esta sala no tiene descripción."
        if len(self.session.user.room.exits) > 0:
            exits = '  '+('\n\r  '.join(["{}".format(exit) for exit in self.session.user.room.exits.keys()]))
            exits = "Salidas:\n\r{}".format(exits)
        else:
            exits = "No hay ningún camino para salir de esta habitación (pero podrías ser el primero en crear uno)."
        players_here = '\n\r'.join(['{} está aquí.'.format(user.name) for user in User.objects(room=self.session.user.room, client_id__ne=None) if user != self.session.user])
        message = "Estás en {}.\n\r{}\n\r{}\n\r{}".format(title, description, exits, players_here)
        self.session.send_to_client(message)