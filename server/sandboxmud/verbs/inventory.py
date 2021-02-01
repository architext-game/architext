from .verb import Verb
from .. import util
import functools

class Take(Verb):
    '''Takes a item to your inventory.
    usage:
        command item_name
    '''

    command = 'coger '

    def process(self, message):
        partial_name = message[len(self.command):]
        names_of_takable_items = [item.name for item in self.session.user.room.items if item.is_takable()]
        items_they_may_be_referring_to = util.possible_meanings(partial_name, names_of_takable_items)

        if len(items_they_may_be_referring_to) < 1:
            self.session.send_to_client('No hay un objeto con ese nombre que puedas coger.')
        elif len(items_they_may_be_referring_to) > 1:
            self.session.send_to_client('Hay más de un objeto con ese nombre. Sé más específico.')
        else:
            target_item_name = items_they_may_be_referring_to[0]
            target_item = next(filter(lambda i: i.name==target_item_name, self.session.user.room.items))
            self.session.user.add_item_to_inventory(target_item)
            self.session.user.room.remove_item(target_item)
            self.session.send_to_client('Has cogido el objeto.')
        
        self.finish_interaction()


class Drop(Verb):
    '''Drops a item from your inventory.
    usage:
        command item_name
    '''

    command = 'dejar '

    def process(self, message):
        partial_name = message[len(self.command):]
        names_of_dropable_items = [item.name for item in self.session.user.inventory]
        items_they_may_be_referring_to = util.possible_meanings(partial_name, names_of_dropable_items)

        if len(items_they_may_be_referring_to) < 1:
            self.session.send_to_client('No hay un objeto con ese nombre en tu inventario.')
        elif len(items_they_may_be_referring_to) > 1:
            self.session.send_to_client('Hay más de un objeto con ese nombre en tu inventario. Sé más específico.')
        else:
            target_item_name = items_they_may_be_referring_to[0]
            target_item = next(filter(lambda i: i.name==target_item_name, self.session.user.inventory))
            self.session.user.remove_item_from_inventory(target_item)
            self.session.user.room.add_item(target_item)
            self.session.send_to_client('Has dejado el objeto.')
        
        self.finish_interaction()


class Inventory(Verb):
    '''Shows what you have in your inventory'''

    command = 'inventario'

    def process(self, message):
        if len(self.session.user.inventory) < 1:
            self.session.send_to_client('No tienes ningún objeto en tu inventario.')
        else:
            item_names = [item.name for item in self.session.user.inventory]
            inventory_list = functools.reduce(lambda a, b: '{}\n{}'.format(a,b), item_names)
            self.session.send_to_client('Llevas contigo estos objetos:\n{}'.format(inventory_list))

        self.finish_interaction()