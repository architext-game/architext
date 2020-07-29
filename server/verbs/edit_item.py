from .verb import Verb

class EditItem(Verb):
    """This verb allows users to edit the description of an item that is in their current room"""

    command = 'editar '

    def __init__(self, session):
        super().__init__(session)
        self.option_number = None
        self.current_process_function = self.start_editing_item

    def process(self, message):
        self.current_process_function(message)

    def start_editing_item(self, message):
        message = message[len(self.command):]
        if message in [item.name for item in self.session.user.room.items]:
            self.item_to_edit = message
            self.session.send_to_client("Introduce la nueva descripción para el objeto {}".format(message))
            self.current_process_function = self.process_item_description
        else:
            self.session.send_to_client("No encuentras ese objeto.")
            self.finish_interaction()

    def process_item_description(self, message):
        for item in self.session.user.room.items:
            if item.name == self.item_to_edit:
                item.description = message
                item.save()
                break
        self.session.send_to_client("Hecho.")
        self.finish_interaction()