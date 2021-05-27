from .verb import Verb

class Exits(Verb):
    """This verb shows users all exits that are not hidden"""
    command = _('exits')

    def process(self, message):
        exits_names = [exit.name for exit in self.session.user.room.exits if not exit.is_hidden()]

        if exits_names:
            out_message =_('Obvious exits:') + '\n ⮕ ' + '\n ⮕ '.join(exits_names)
        else:
            out_message = _('There is not an obvious way to exit this room.')

        self.session.send_to_client(out_message)
        self.finish_interaction()