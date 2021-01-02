from .verb import Verb
import functools

class PlaceItem(Verb):
    command = "colocar"
    
    def __init__(self, session):
        super().__init__(session)
        self.current_process_function = self.process_first_message

    def process(self, message):
        self.current_process_function(message)

    def process_first_message(self, message):
        saved_item_names_and_indexes = ["{}. {}".format(index, item.name) for index, item in enumerate(self.session.user.saved_items)]
        saved_item_list = functools.reduce(lambda a, b: '{}\n{}'.format(a,b), saved_item_names_and_indexes)
        self.session.send_to_client('¿Qué objeto quieres colocar?\n{}'.format(saved_item_list))
        self.current_process_function = self.process_item_choice

    def process_item_choice(self, message):
        try:
            message = int(message)
        except ValueError:
            self.session.send_to_client('Debes introducir un número.')
            return

        max_number = len(self.session.user.saved_items)
        if 0 <= message < max_number:
            item_to_place = self.session.user.saved_items[message].clone()
            self.session.user.room.add_item(item_to_place)
            self.session.send_to_client('Hecho!')
        else:
            self.session.send_to_client('Debes introducir el número correspondiente a uno de tus objetos guardados.')

        self.finish_interaction()


class SaveItem(Verb):
    command = 'guardar '

    def process(self, message):
        message = message[len(self.command):]
        selected_item = next(filter(lambda i: i.name==message, self.session.user.room.items), None)
        if selected_item is not None:
            self.session.user.save_item(selected_item)
            self.session.send_to_client("Hecho.")
        else:
            self.session.send_to_client("No existe ese objeto en esta habitación.")
        self.finish_interaction()

        
