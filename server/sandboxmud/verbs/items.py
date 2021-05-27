from .verb import Verb

class Items(Verb):
    """This verb shows users all items that are not hidden"""
    command = _('items')

    def process(self, message):
        items_names = [item.name for item in self.session.user.room.items if not item.is_hidden()]

        if items_names:
            out_message = _('Obvious items:\n ● ') + f'\n {chr(9679)} '.join(items_names)
        else:
            out_message = _('At first glance, it seems there is nothing here.')

        self.session.send_to_client(out_message)
        self.finish_interaction()