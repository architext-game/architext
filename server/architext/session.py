"""Defines the Session class, used to handle user interaction.
"""
from . import verbs as v
from . import util
import textwrap
from architext.adapters.sender import AbstractSender
from architext.adapters.repository import AbstractRepository

class Session:
    """This class handles interaction with a single user, though it can send messages to other users as well, to inform them of the session's user actions.
    The Session is responsible for:
      - Redirecting messages sent by its client to the right verb to process them.
      - Provide methods to verbs for sending messages from the client's perspective: only to the client, to other users in the client's room, etc.
      - Asking verbs if the interaction is finished so it can keep using the verb to process messages or poll again for a new verb.
      - Handle client disconnection.
    """

    # List of all verbs supported by the session, ordered by priority: if two verbs can handle the same message, the first will have preference.
    verbs = [v.Build, v.Go, v.Look]

    def __init__(self, sender: AbstractSender, repository: AbstractRepository, connection_id: str):
        self.logger = None  # logger for recording user interaction
        self.sender = sender  # server used to send messages
        self.repository = repository
        self.current_verb = v.Login(self)  # verb that is currently handling interaction. It starts with the log-in process.
        self.user_id: str | None = None  # here we'll have an User id once the log-in is completed.
        self.world_list_cache = None  # when the lobby is shown its values are cached here (see #122).
        self.connection_id = connection_id

    def process_message(self, message):
        """This method processes a message sent by the client.
        It polls all verbs, using their can_process method to find a verb that can process the message.
        Then makes that verb the current_verb and lets it handle the message.
        """
        if self.logger:
            self.logger.info('client\n'+message)

        if self.current_verb is None:
            for verb in self.verbs:
                if verb.can_process(message, self):
                    self.current_verb = verb(self)
                    break

        if self.current_verb is not None:
            try:
                self.current_verb.execute(message)
            except Exception as e:
                self.sender.send_to_client(_("An unexpected error ocurred. It has been notified and it will be soon fixed. You probably can continue playing without further issues."))
                if self.logger: self.logger.exception('ERROR: ' + str(e))
                raise e

            if self.current_verb.command_finished():
                self.current_verb = None
        else:
            if False and self.user.room is None:  # TODO
                self.sender.send_to_client(_('I don\'t understand that. You can enter "r" to show the lobby menu again.'))
            else:
                self.sender.send_to_client(_('I don\'t understand that.'))

    def disconnect(self):
        if self.user_id is not None:
            if not self.repository.get_user(self.user_id).master_mode:
                self.sender.send_to_others_in_room(_("Whoop! {player_name} has gone.").format(player_name=self.user.name))
            # self.user.disconnect()  # TODO
        self.client_id = None

    def set_logger(self, logger):
        self.logger = logger


class GhostSession(Session):  # TODO
    """This is a ghost session that the system uses to perform automated tasks
    like player defined verbs. The tasks are executed as normal messages that
    a ghost session processes as if it were a normal session.

    The differences whith a normal session are:
     - A ghost session doesn't respond to the client that is issuing it
       messages, because there is none.
     - A ghost session belongs to the user specified in the field GHOST_USER_NAME.
       This user cannot be used by normal sessions.
     - A ghost session ends as soon as the automated task does.
    """

    MAX_DEPTH = 10  # max number of recursive GhostSessions

    def __init__(self, server, start_room, creator_session, depth=0):
        GHOST_USER_NAME = util.GHOST_USER_NAME  # name of the ghost user
        PLACEHOLDER_SESSION_ID = -1  # with this invalid id, the server won't send messages meant to the session's client 
        super().__init__(PLACEHOLDER_SESSION_ID, server)  # normal session __init__. Assigns session id and server.
        self.current_verb = None  # we want to not have an assigned verb at session creation.
        self.depth = depth
        self.creator_session = creator_session
        if self.depth > self.MAX_DEPTH:
            raise GhostSessionMaxDepthExceeded()

        # retrieve or create ghost user and put in in the right room.
        if entities.User.objects(name=GHOST_USER_NAME):
            self.user = entities.User.objects(name=GHOST_USER_NAME).first()
            self.user.connect(self.client_id)
            self.user.teleport(start_room)
        else:
            self.user = entities.User(name=GHOST_USER_NAME, room=start_room, master_mode=True, password='patata frita')
            self.user.connect(self.client_id)

    def disconnect(self):
        if self.user is not None:
            self.user.disconnect()


class GhostSessionMaxDepthExceeded(Exception):
    """
    Raised when there are too many nested custom verbs in execution.
    i.e. when a custom verb is used that uses another custom verb, and so on.
    """