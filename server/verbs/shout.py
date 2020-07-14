from .verb import Verb

class Shout(Verb):
    command = 'gritar '

    def process(self, message):
        command_length = len(self.command)
        out_message = '{} grita "{}"'.format(self.session.user.name, message[command_length:])
        self.session.send_to_all(out_message)
        self.finished = True