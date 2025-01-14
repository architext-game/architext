from gettext import gettext as _
from architext.core import Architext
from .. import util

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from architext.chatbot.session import Session
else:
    Session = object()



FREE = 'free'
PRIVILEGED = 'privileged'
CREATOR = 'creator'
NOBOT = 'nobot'

class Verb():
    """This is the template for creating new verbs. Every verb should have Verb as parent.
    This is an abstract class, with some methods not implemented.

    A verb is every action that a user can take in the world. Each verb object processes
    a fixed set of user messages, and takes all the actions relative to them.

    Each verb has its own criteria that determines if it can process a given message. This
    criteria is defined in its can_process(message) method. The session calls the can_process method
    of each verb in its verb list until it finds a verb that can process the message. 

    Then, the session creates a new instance of the verb and lets it process all user messages
    (via the process(message) method) until the verb instance returns True for its method command_finished.
    """

    command = 'verb '
    permissions = FREE  # possible values: FREE, PRIVILEGED, NOBOT and CREATOR.
    regex_command = False  # False: can process if message starts with command. True: command is a regex and can process if message matches the regex.

    @classmethod
    def message_matches_command(cls, message: str):
        if cls.regex_command:
            return util.match(cls.command, message) is not None
        else:
            if type(cls.command) == str:
                if message.startswith(cls.command):
                    return True
            elif type(cls.command) == list:
                for command in cls.command:
                    if message.startswith(command):
                        return True 
            
            return False

    @classmethod
    def can_process(cls, message: str, session: Session):
        return cls.message_matches_command(message)

    def __init__(self, session: Session, architext: Architext):
        self.session = session
        self.architext = architext
        self.finished = False

    def execute(self, message: str):
        if self.user_has_enough_privileges():
            self.process(message)
        else:
            self.session.sender.send(self.session.user_id, _('You don\'t have enough privileges to do that here.'))
            self.finish_interaction()

    def user_has_enough_privileges(self) -> bool:
        return True  # TODO

        # if self.session.user is None:
        #     return True

        # if self.session.user.room is None:
        #     return True

        # world = self.session.user.room.world_state.get_world()
        
        # if self.permissions == FREE:
        #     return True

        # if self.permissions == NOBOT:
        #     if isinstance(self.session, session.GhostSession):
        #         return False
        #     else:
        #         return True
        
        # if self.permissions == PRIVILEGED:
        #     if world.all_can_edit or isinstance(self.session, session.GhostSession) or world.is_privileged(self.session.user):
        #         return True
        #     else:
        #         return False
        
        # if self.permissions == CREATOR:
        #     if world.is_creator(self.session.user):
        #         return True
        #     else:
        #         return False

    def process(self, message: str):
        raise Exception('Abstract method of interface Verb not implemented')

    def command_finished(self) -> bool:
        return self.finished

    def finish_interaction(self) -> None:
        """This method must be called from within the Verb when the interaction is finished, so the session
        can pass command to other verbs"""
        self.finished = True