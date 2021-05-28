from .verb import Verb
from .look import Look
from . import lobby
from .. import entities
from .. import util
import logging
import textwrap
from .. import strings

class Login(Verb):
    """This is the first verb that a session starts with, and handles user log-in.
    After that, users can't use this verb, and it should not be in the session's verb list.
    """

    def __init__(self, session):
        super().__init__(session)
        out_message  = _("""
                ___       __   __         ___    ___  __  
          |  | |__  |    /  ` /  \  |\/| |__      |  /  \ 
          |/\| |___ |___ \__, \__/  |  | |___     |  \__/ 
     
   █████  ██████   ██████ ██   ██ ██ ████████ ███████ ██   ██ ████████  
  ██   ██ ██   ██ ██      ██   ██ ██    ██    ██       ██ ██     ██     
  ███████ ██████  ██      ███████ ██    ██    █████     ███      ██     
  ██   ██ ██   ██ ██      ██   ██ ██    ██    ██       ██ ██     ██     
  ██   ██ ██   ██  ██████ ██   ██ ██    ██    ███████ ██   ██    ██ 
  ────────────────────────────────────────────────────────────────────
                 ╔╦╗╦ ╦╔═╗  ╔═╗╔═╗╔╗╔╔╦╗╔╗ ╔═╗═╗ ╦
                  ║ ╠═╣║╣   ╚═╗╠═╣║║║ ║║╠╩╗║ ║╔╩╦╝
                  ╩ ╩ ╩╚═╝  ╚═╝╩ ╩╝╚╝═╩╝╚═╝╚═╝╩ ╚═

""")
        out_message += util.get_config()['cover']
        out_message += _("\n\n\n ᐅ What is your nickname?")
        self.session.send_to_client(out_message)

        self.current_process_function = self.process_user_name

    def process(self, message):
        self.current_process_function(message)

    def process_user_name(self, message):
        if not message:
            self.session.send_to_client(strings.is_empty)
        elif message == util.GHOST_USER_NAME:
            self.session.send_to_client(_("That name is reserved. Try with another one."))
        elif '\n' in message:
            self.session.send_to_client(strings.has_line_breaks)
        elif len(message) > entities.User.NAME_MAX_LENGTH:
            self.session.send_to_client(_("The name can\'t exceed {character_limit} characters.").format(character_limit=entities.User.NAME_MAX_LENGTH))
        else:
            self.selected_user = next(entities.User.objects(name=message), None)

            # returning user or new user entering a name in use
            if self.selected_user:
                self.session.send_to_client(_(
                    'An avatar with that name already exists.\n'
                    ' ᐅ Enter {user_name}\'s password or "/" to go back.'
                ).format(user_name=message))
                self.current_process_function = self.process_login_password

            # new user or returning user mispelling its name
            else:
                self.new_name = message
                self.session.send_to_client(_(
                    'That name is not in use.\n'
                    ' ᐅ To create a new account with this name, enter a password.\n'
                    ' ᐅ To go back, enter "/"'
                ))
                self.current_process_function = self.process_sign_in_password        

    def process_login_password(self, message):
        if message == '/':
            self.session.send_to_client(_(
                ' ᐅ What is your nickname?'
            ))
            self.current_process_function = self.process_user_name
            return

        if True:  # correct password case
            self.session.user = self.selected_user
            self.session.send_to_client(util.get_config()['log_in_welcome'])
            self.connect()
            self.finish_interaction()
        else:
            self.session.send_to_client(_(
                'That password is not correct.\n'
                ' ᐅ What is your nickname?'
            ))
            self.current_process_function = self.process_user_name

    def process_sign_in_password(self, message):
        if message == '/':
            self.session.send_to_client(_(
                ' ᐅ What is your nickname?'
            ))
            self.current_process_function = self.process_user_name
            return
        if len(message) < 6:
            self.session.send_to_client(_(
                'The password needs to have six or more characters. Try with another one.'
            ))
            return
        self.password = message
        self.session.send_to_client(_('Enter your password again to confirm.'))
        self.current_process_function = self.process_repeat_log_in_password

    def process_repeat_log_in_password(self, message):
        if message != self.password:
            self.session.send_to_client(_(
                'The two passwords don\'t match.\n'
                ' ᐅ What is your nickname?'
            ))
            self.current_process_function = self.process_user_name
            return

        self.session.user = entities.User(name=self.new_name, room=None)
        self.session.send_to_client(util.get_config()['sign_in_welcome'])
        self.connect()
        self.finish_interaction()
        

    def connect(self):
        self.session.user.connect(self.session.client_id)
        self.session.user.leave_master_mode()
        # logger setup
        name = self.session.user.name
        server_logger = logging.getLogger('server_logger')
        user_logger = util.setup_logger('user_'+name, 'user_'+name+'.txt')
        self.session.set_logger(user_logger)
        # log user connection
        log_message = '{} has connected.'.format(name)
        user_logger.info(log_message)
        server_logger.info(log_message)

        self.session.send_to_client(_(
            'LOGGED IN AS:     {user_name}\n'
            'YOU ARE IN:       {location}\n'
            'ONLINE USERS:     {user_count}'
        ).format(
            user_name=self.session.user.name,
            location=(
                _('the lobby')
                if self.session.user.room is None else
                _('{room_name} ─ {world_name}').format(room_name=self.session.user.room.name, world_name=self.session.user.room.world_state.get_world().name)
            ),
            user_count=len(entities.User.objects(client_id__ne=None))
        ))
        if self.session.user.room is not None:
            self.session.send_to_others_in_room(_("Poohf! {user_name} appears.").format(user_name=name))
            Look(self.session).show_current_room()
        else:
            lobby.LobbyMenu(self.session).show_lobby_menu()
