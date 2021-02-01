from .verb import Verb

class Items(Verb):
    """This verb shows users all items that are not hidden"""
    command = 'objetos'

    def process(self, message):
        items_names = [item.name for item in self.session.user.room.items if not item.is_hidden()]

        if items_names:
            out_message = 'Distingues fácilmente los siguientes objetos:\n  ' + '\n  '.join(items_names)
        else:
            out_message = 'A primera vista parece que no hay ningún objeto interesante en esta sala.'

        self.session.send_to_client(out_message)
        self.finish_interaction()