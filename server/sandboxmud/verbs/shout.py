from .verb import Verb

class Shout(Verb):
    """Let players send messages to every player connected in the same world"""

    command = 'gritar '

    def process(self, message):
        command_length = len(self.command)
        out_message = f'{self.session.user.name} grita "¡¡{message[command_length:].upper()}!!"'
        self.session.send_to_all(out_message)
        self.finish_interaction()