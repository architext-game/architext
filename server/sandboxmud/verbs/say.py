from .verb import Verb

class Say(Verb):
    """Lets players send messages to people on the same room"""

    command = _('say ')

    def process(self, message):
        command_length = len(self.command)
        out_message = '{} says "{}"'.format(self.session.user.name, message[command_length:])
        self.session.send_to_room(out_message)
        self.finish_interaction()