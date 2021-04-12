from .verb import Verb
from .. import util
import functools
from .. import entities

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
            self.session.user.get_current_world_inventory().add_item(target_item)
            target_item.remove_from_room()
            self.session.send_to_client(f'Has cogido {target_item_name}.')
        
        self.finish_interaction()


class Drop(Verb):
    '''Drops a item from your inventory.
    usage:
        command item_name
    '''

    command = 'dejar '

    def process(self, message):
        partial_name = message[len(self.command):]
        names_of_dropable_items = [item.name for item in self.session.user.get_current_world_inventory().items]
        items_they_may_be_referring_to = util.possible_meanings(partial_name, names_of_dropable_items)

        if len(items_they_may_be_referring_to) < 1:
            self.session.send_to_client('No hay un objeto con ese nombre en tu inventario.')
        elif len(items_they_may_be_referring_to) > 1:
            self.session.send_to_client('Hay más de un objeto con ese nombre en tu inventario. Sé más específico.')
        else:
            target_item_name = items_they_may_be_referring_to[0]
            target_item = next(filter(lambda i: i.name==target_item_name, self.session.user.get_current_world_inventory().items))
            self.session.user.get_current_world_inventory().remove_item(target_item)
            target_item.put_in_room(self.session.user.room)
            self.session.send_to_client(f'Has dejado {target_item_name}.')
        
        self.finish_interaction()


class Inventory(Verb):
    '''Shows what you have in your inventory'''

    command = 'inventario'

    def process(self, message):
        if len(self.session.user.get_current_world_inventory().items) < 1:
            self.session.send_to_client('No tienes ningún objeto en tu inventario.')
        else:
            item_names = [item.name for item in self.session.user.get_current_world_inventory().items]
            item_list_items = [f'{chr(9679)} {name}' for name in item_names]
            inventory_list = '\n'.join(item_list_items)
            self.session.send_to_client(f'Llevas contigo estos objetos:\n{inventory_list}')

        self.finish_interaction()


class Give(Verb):
    command = "dar '"

    def process(self, message):
        message = message[len(self.command):]
        target_user_name, target_item_name = message.split("' ", 1)

        target_user = next(entities.User.objects(name=target_user_name, room=self.session.user.room, client_id__ne=None), None)
        item = next(entities.Item.objects(name=target_item_name, room=self.session.user.room, visible='takable'), None)

        if target_user is not None and item is not None:
            target_user.get_current_world_inventory().add_item(item)
            self.session.send_to_client('Hecho.')
        else:
            self.session.send_to_client("El usuario u objeto no está en esta sala.")

        self.finish_interaction()

class TakeFrom(Verb):
    command = "quitar '"

    def process(self, message):
        message = message[len(self.command):]
        target_user_name, target_item_name = message.split("' ", 1)

        target_user = next(entities.User.objects(name=target_user_name, room=self.session.user.room, client_id__ne=None), None)
        
        if target_user is not None:
            target_item = next(filter(lambda i: i.name==target_item_name, target_user.get_current_world_inventory().items), None)
            if target_item is not None:
                target_user.get_current_world_inventory().remove_item(target_item)
                target_item.put_in_room(target_user.room)
                self.session.send_to_client('Hecho.')
            else:
                self.session.send_to_client('El objeto no está en el inventario de ese usuario.')
        else:
            self.session.send_to_client('Ese usuario no está aquí.')

        self.finish_interaction()