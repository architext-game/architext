from .verb import Verb
from .look import Look
from . import lobby
from .. import entities
from .. import util
import logging
import textwrap

class Login(Verb):
    """This is the first verb that a session starts with, and handles user log-in.
    After that, users can't use this verb, and it should not be in the session's verb list.
    """

    def __init__(self, session):
        super().__init__(session)
        cover = util.get_config()['cover']
        self.session.send_to_client(str(cover))
        self.session.send_to_client(_("What is your character name? (or the name for your new character)\n\r"))
        self.current_process_function = self.start_login

    def process(self, message):
        self.current_process_function(message)

    def start_login(self, message):
        if message == util.GHOST_USER_NAME:
            self.session.send_to_client(_("That name is reserved. Try with another one."))
            return

        try:
            self.process_user_name(message)
        except entities.EmptyName:
            self.session.send_to_client(strings.is_empty)
        except entities.ValueWithLineBreaks:
            self.session.send_to_client(strings.has_line_breaks)
        except entities.ValueTooLong:
            self.session.send_to_client(_("The name can\'t exceed {character_limit} characters.").format(character_limit=entities.User.NAME_MAX_LENGTH))


    def process_user_name(self, name):
        out_message = ''

        # returning user
        if entities.User.objects(name=name):
            self.session.user = entities.User.objects(name=name).first()
            self.session.user.connect(self.session.client_id)
            out_message += util.get_config()["old_user_welcome_message"]
        # new user
        else:
            starting_room = None
            self.session.user = entities.User(name=name, room=starting_room)
            self.session.user.connect(self.session.client_id)
            out_message += util.get_config()["new_user_welcome_message"]

        self.session.user.leave_master_mode()

        out_message += '\n' + self.get_status_message()

        if self.session.user.room is not None:
            self.session.send_to_others_in_room(_("Poohf! {user_name} appears.").format(user_name=name))
            world = self.session.user.room.world_state.get_world()

        out_message += _("\nPress enter to continue...")        
        self.session.send_to_client(out_message)

        self.current_process_function = self.process_enter_to_continue

        # logger setup
        server_logger = logging.getLogger('server_logger')
        user_logger = util.setup_logger('user_'+name, 'user_'+name+'.txt')
        self.session.set_logger(user_logger)
        # log user connection
        log_message = '{} has connected.'.format(name)
        user_logger.info(log_message)
        server_logger.info(log_message)

    def process_enter_to_continue(self, message):
        if self.session.user.room is not None:
            Look(self.session).show_current_room()
        else:
            lobby.LobbyMenu(self.session).show_lobby_menu()
        self.finish_interaction()

    def get_status_message(self):
        return _(
            'You are logged in as {user_name}.\n'
            'You are in {location}.'
        ).format(user_name=self.session.user.name, location=self.get_location())

    def get_location(self):
        user = self.session.user
        if user.room is None:
            return _('the lobby')
        else:
            world = user.room.world_state.get_world()
            return _('the world {world_name}, by {creator_name}').format(world_name=world.name, creator_name=world.creator.name)