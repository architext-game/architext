from .verb import Verb

class Exits(Verb):
    """This verb shows users all exits that are not hidden"""
    command = 'salidas'

    def process(self, message):
        exits_names = [exit.name for exit in self.session.user.room.exits if not exit.hidden()]

        if exits_names:
            out_message = 'Fácilmente distingues las siguientes salidas:\n  ' + '\n'.join(exits_names)
        else:
            out_message = 'No hay ninguna manera obvia de salir de esta habitación.'

        self.session.send_to_client(out_message)
        self.finish_interaction()