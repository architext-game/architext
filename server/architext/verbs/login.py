from .verb import Verb
from .look import Look
# from . import lobby
from .. import util
import logging
import textwrap
import architext.resources.tutorial_world as tutorial_world
import architext.resources.monks_riddle as monks_riddle
from .. import strings
import architext.service_layer.goodservices as services
from architext.adapters.sender import AbstractSender
from architext.adapters.repository import AbstractRepository
import architext.domain.model as model

USER_NAME_MAX_LENGTH = 26

class Login(Verb):
    """This is the first verb that a session starts with, and handles user log-in.
    After that, users can't use this verb, and it should not be in the session's verb list.
    """

    def __init__(self, session):
        super().__init__(session=session)
        out_message  = _("""
                ___       __   __         ___    ___  __  
          |  | |__  |    /  ` /  \\  |\\/| |__      |  /  \\ 
          |/\\| |___ |___ \\__, \\__/  |  | |___     |  \\__/ 
     
   █████  ██████   ██████ ██   ██ ██ ████████ ███████ ██   ██ ████████
  ██   ██ ██   ██ ██      ██   ██ ██    ██    ██       ██ ██     ██   
  ███████ ██████  ██      ███████ ██    ██    █████     ███      ██   
  ██   ██ ██   ██ ██      ██   ██ ██    ██    ██       ██ ██     ██   
  ██   ██ ██   ██  ██████ ██   ██ ██    ██    ███████ ██   ██    ██ 

  ╔══╤═══╤═══╤══╤═══╦╗╦ ╦╔═╗  ╔═╗╔═╗╔╗╔╔╦╗╔╗ ╔═╗═╗ ╦══════╤═╤═══╤╤══╤╗
  ╟──┴┬─┬┘ ┌─┴┬─┘   ║ ╠═╣║╣   ╚═╗╠═╣║║║ ║║╠╩╗║ ║╔╩╦╝   ┌──┴─┼──┬┴┴┬─┘║
  ╚═══╧═╧══╧══╧═════╩ ╩ ╩╚═╝  ╚═╝╩ ╩╝╚╝═╩╝╚═╝╚═╝╩ ╚════╧════╧══╧══╧══╝

""")
        cover = util.get_config()['cover']
        out_message += cover if cover else strings.default_cover
        out_message += _("\n\n\n ᐅ What is your nickname?")
        self.session.sender.send_to_client(out_message)

        self.current_process_function = self.process_user_name

    def process(self, message):
        self.current_process_function(message)

    def process_user_name(self, message):
        if not message:
            self.session.sender.send_to_client(strings.is_empty)
        elif message == util.GHOST_USER_NAME:
            self.session.sender.send_to_client(_("That name is reserved. Try with another one."))
        elif '\n' in message:
            self.session.sender.send_to_client(strings.has_line_breaks)
        elif len(message) > USER_NAME_MAX_LENGTH:
            self.session.sender.send_to_client(_("The name can\'t exceed {character_limit} characters.").format(character_limit=USER_NAME_MAX_LENGTH))
        else:
            self.selected_user = self.session.repository.get_user_by_name(message)

            # returning user or new user entering a name in use
            if self.selected_user:
                self.session.sender.send_to_client(_(
                    'An avatar with that name already exists.\n'
                    ' ᐅ Enter {user_name}\'s password or "/" to go back.'
                ).format(user_name=message))
                self.current_process_function = self.process_login_password

            # new user or returning user mispelling its name
            else:
                self.new_name = message
                self.session.sender.send_to_client(_(
                    'That name is not in use.\n'
                    ' ᐅ To create a new account with this name, enter a password.\n'
                    ' ᐅ To go back, enter "/"'
                ))
                self.current_process_function = self.process_sign_in_password        

    def process_login_password(self, message):
        if message == '/':
            self.session.sender.send_to_client(_(
                ' ᐅ What is your nickname?'
            ))
            self.current_process_function = self.process_user_name
            return

        if self.selected_user.match_password(message):
            self.session.user_id = self.selected_user
            log_in_welcome = util.get_config()['log_in_welcome']
            log_in_welcome = log_in_welcome if log_in_welcome else strings.default_log_in_welcome
            self.session.sender.send_to_client(log_in_welcome)
            self.connect()
            self.finish_interaction()
        else:
            self.session.sender.send_to_client(_(
                'That password is not correct.\n'
                ' ᐅ What is your nickname?'
            ))
            self.current_process_function = self.process_user_name

    def process_sign_in_password(self, message):
        if message == '/':
            self.session.sender.send_to_client(_(
                ' ᐅ What is your nickname?'
            ))
            self.current_process_function = self.process_user_name
            return
        if len(message) < 6:
            self.session.sender.send_to_client(_(
                'The password needs to have six or more characters. Try with another one.'
            ))
            return
        self.password = message
        self.session.sender.send_to_client(_('Enter your password again to confirm.'))
        self.current_process_function = self.process_repeat_password

    def process_repeat_password(self, message):
        if message != self.password:
            self.session.sender.send_to_client(_(
                'The two passwords don\'t match.\n'
                ' ᐅ What is your nickname?'
            ))
            self.current_process_function = self.process_user_name
            return

        self.session.sender.send_to_client(_(
             'ᐅ What is your email? (Optional, used for password recovery and important communications)\n'
        ))
        self.current_process_function = self.process_email

    def process_email(self, message):
        # check if this is the first user in the server
        is_first_user = self.session.repository.is_server_virgin()

        # create user
        user_id = services.create_user(repository=self.session.repository, name=self.new_name, password=self.password, email=message)
        self.session.user_id = user_id
        # if is first user, create common worlds.
        if False and is_first_user:  # TODO
            self.session.sender.send_to_client(_(
                "This is the first account created in this server. It has been established as the administrator account.\n"
                "This means that the public worlds that are going to be created now will be yours.\n\n"
                "Creating initial worlds..."
            ))
            services.new_world_from_json(self.session, _('The Monk\'s Riddle'), monks_riddle.json)
        # create tutorial world and move the user there
        sign_in_welcome = util.get_config()['sign_in_welcome']
        sign_in_welcome = sign_in_welcome if sign_in_welcome else strings.default_sign_in_welcome
        self.session.sender.send_to_client(sign_in_welcome)
        self.session.sender.send_to_client(_("Building your Museum of Architexture..."))

        # starting_world = services.new_world_from_json(self.session, _('The Museum of Architexture'), tutorial_world.json)  # TODO
        world_id = services.create_world(
            user_id=user_id,
            repository=self.session.repository,
            name='First World',
            room_name='First Room',
            room_description='This is the first room'
        )
        services.enter_world(
            repository=self.session.repository,
            user_id=user_id,
            world_id=world_id
        )

        self.connect()
        self.finish_interaction()


    def connect(self):
        # self.session.user.leave_master_mode()  # TODO
        # logger setup
        user = self.session.repository.get_user(self.session.user_id)
        room = self.session.repository.get_user_room(self.session.user_id)
        world = self.session.repository.get_world_by_state_id(room.world_state_id)
        server_logger = logging.getLogger('server_logger')
        user_logger = util.setup_logger('user_'+user.name, 'user_'+user.name+'.txt')
        self.session.set_logger(user_logger)
        # log user connection
        log_message = '{} has logged in from client_id {}.'.format(user.name, 'unknown')
        user_logger.info(log_message)
        server_logger.info(log_message)

        services.connect(repository=self.session.repository, user_id=user.id, connection_id=self.session.connection_id)

        self.session.sender.send_to_client(_(
            'LOGGED IN AS:     {user_name}\n'
            'YOU ARE IN:       {location}\n'
            'ONLINE USERS:     {user_count}'
        ).format(
            user_name=user.name,
            location=(
                _('the lobby')
                if room is None else
                _('{room_name} ─ {world_name}').format(room_name=room.name, world_name=world.name)
            ),
            user_count='todo'  # TODO
        ))
        if room is not None:
            self.session.sender.send_to_others_in_room(_("Poohf! {user_name} appears.").format(user_name=user.name))
            Look(self.session).show_current_room(show_world_name=True)
        else:
            # lobby.LobbyMenu(self.session).show_lobby_menu()  # TODO
            pass
