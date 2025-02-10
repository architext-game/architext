"""Defines the Session class, used to handle user interaction.
"""
from architext.chatbot.sender import Sender
from architext.core import Architext
from . import verbs as v
from .verbs import Verb
from architext.chatbot.ports.messaging_channel import MessagingChannel
from architext.chatbot.ports.logger import Logger
from typing import Type, List, Optional
from gettext import gettext as _

class Session:
    """This class handles interaction with a single user, though it can send messages to other users as well, to inform them of the session's user actions.
    The Session is responsible for:
      - Redirecting messages sent by its client to the right verb to process them.
      - Provide methods to verbs for sending messages from the client's perspective: only to the client, to other users in the client's room, etc.
      - Asking verbs if the interaction is finished so it can keep using the verb to process messages or poll again for a new verb.
      - Handle client disconnection.
    """

    # List of all verbs supported by the session, ordered by priority: if two verbs can handle the same message, the first will have preference.
    verbs: List[Type[Verb]] = [v.Look, v.Build, v.Go, v.Exits, v.Info, v.Link, v.Edit, v.Items, v.Delete, v.Raze, v.EditRoom]

    def __init__(self, user_id: str, messaging_channel: MessagingChannel, logger: Logger, architext: Architext):
        self.architext = architext
        self.sender = Sender(architext=architext, channel=messaging_channel)
        self.logger = logger  # logger for recording user interaction
        self.user_id = user_id  # id of the user whose messages this is processing
        self.current_verb: Optional[Verb] = None  # verb that is currently handling interaction. It starts with the log-in process.
        self.user = None  # here we'll have an User entity once the log-in is completed.
        self.world_list_cache = None  # when the lobby is shown its values are cached here (see #122).

    def process_message(self, message: str):
        """This method processes a message sent by the client.
        It polls all verbs, using their can_process method to find a verb that can process the message.
        Then makes that verb the current_verb and lets it handle the message.
        """
        message = message.strip()
        if self.user is not None:
            self.user.reload()
            if self.user.user_id != self.user_id:  # another session has been opened for the same user
                self.send_to_client('Otra sesión ha sido abierta para el mismo usuario. Tu sesión ha sido cerrada.')
                self.disconnect()
                return

        if self.logger:
            self.logger.log('client\n'+message)
        
        if self.current_verb is None:
            for verb in self.verbs:
                if verb.can_process(message, self):
                    self.current_verb = verb(self, self.architext)
                    break
        
        if self.current_verb is not None:
            try:
                self.current_verb.execute(message)
            except Exception as e:
                self.sender.send(self.user_id, _("An unexpected error ocurred. It has been notified and it will be soon fixed. You probably can continue playing without further issues."))
                if self.logger:
                    self.logger.log('ERROR: ' + str(e))
                else:
                    print('ERROR: ' + str(e))
                raise e
            
            if self.current_verb.command_finished():
                self.current_verb = None
        else:
            self.sender.send(self.user_id, _('I don\'t understand that.'))

    def disconnect(self):
        if self.user is not None and self.user.user_id == self.user_id:
            if not self.user.master_mode:
                self.send_to_others_in_room(_("Whoop! {player_name} has gone.").format(player_name=self.user.name))
            self.user.disconnect()
        self.user_id = None
