from .verb import Verb

class Say(Verb):
    command = 'decir '

    def process(self, message):
        command_length = len(self.command)
        out_message = '{} dice "{}"'.format(self.session.user.name, message[command_length:])
        self.session.send_to_room(out_message)
        self.finished = True