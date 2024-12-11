from .verb import Verb, NOBOT
from architext.adapters.sender import MessageOptions

class Say(Verb):
    """Lets players send messages to people on the same room"""

    command = _('say ')
    permissions = NOBOT

    def process(self, message):
        command_length = len(self.command)
        out_message = '{} says "{}"'.format(self.session.user.name, message[command_length:])
        self.session.send_to_room(out_message, options=MessageOptions(section=False))
        self.finish_interaction()