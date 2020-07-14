from .verb import Verb
from .look import Look
from entities import User, Room

class Login(Verb):
    def process(self, message):
        self.process_user_name(message)
        self.finished = True

    def process_user_name(self, name):
        if User.objects(name=name):
            self.session.user = User.objects(name=name).first()
            self.session.user.connect(self.session.session_id)
            self.session.send_to_client("Bienvenido de nuevo {}.".format(name))
        else:
            lobby = Room.objects(name='lobby').first()
            self.session.user = User(name=name, room=lobby)
            self.session.user.connect(self.session.session_id)
            self.session.send_to_client('Bienvenido {}. Si es tu primera vez, escribe "ayuda" para ver una pequeña guía.'.format(name))

        self.session.send_to_others_in_room("¡Puf! {} apareció.".format(name))
        Look(self.session).show_current_room()
