from .verb import Verb

class Emote(Verb):
    """With this verb users can communicate with users in their same room using acts instead of words (kind of).
    The message that follows the command will be displayed to all users in the room, after the users name.
    Example: "emote sits down"
    Message send to all: "Oliver sits down"
    """
    command = 'emote '

    def process(self, message):
        command_length = len(self.command)
        out_message = '{} {}'.format(self.session.user.name, message[command_length:])
        self.session.send_to_room(out_message)
        self.finish_interaction()