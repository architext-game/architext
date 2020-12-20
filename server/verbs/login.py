from .verb import Verb
from .look import Look
from special_words import GHOST_USER_NAME
import entities
import util
import logging

class Login(Verb):
    """This is the first verb that a session starts with, and handles user log-in.
    After that, users can't use this verb, and it should not be in the session's verb list.
    """

    def __init__(self, session):
        super().__init__(session)
        self.session.send_to_client("Estás conectado. ¿Cómo te llamas?\n\r")

    def process(self, message):
        if self.is_a_valid_name(message):
            self.process_user_name(message)
            self.finish_interaction()
        else:
            self.session.send_to_client('Enter a valid name.')

    def process_user_name(self, name):
        if entities.User.objects(name=name):
            self.session.user = entities.User.objects(name=name).first()
            self.session.user.connect(self.session.session_id)
            self.session.send_to_client("Bienvenido de nuevo {}.".format(name))
        else:
            lobby = entities.Room.objects(alias='0').first()
            self.session.user = entities.User(name=name, room=lobby)
            self.session.user.connect(self.session.session_id)
            self.session.send_to_client('Bienvenido {}. Si es tu primera vez, escribe "ayuda" para ver una pequeña guía.'.format(name))

        self.session.send_to_others_in_room("¡Puf! {} apareció.".format(name))
        Look(self.session).show_current_room()

        server_logger = logging.getLogger('server_logger')
        user_logger = util.setup_logger('user_'+name, 'user_'+name+'.txt')
        self.session.set_logger(user_logger)
        log_message = '{} has connected.'.format(name)
        user_logger.info(log_message)
        server_logger.info(log_message)
        


    def is_a_valid_name(self, name):
        if not name == '' and not name == GHOST_USER_NAME:
            return True
        else:
            return False
