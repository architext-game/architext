from .verb import Verb

class Emote(Verb):
    command = 'emote '

    def process(self, message):
        command_length = len(self.command)
        out_message = '{} {}'.format(self.session.user.name, message[command_length:])
        self.session.send_to_room(out_message)
        self.finished = True