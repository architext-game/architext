from .verb import Verb
from .. import util
import functools
from .. import entities
import architext.strings as strings

class Take(Verb):
    '''Takes a item to your inventory.
    usage:
        command item_name
    '''

    command = _('take ')

    def process(self, message):
        partial_name = message[len(self.command):]

        selected_item = util.name_to_entity(self.session, partial_name, substr_match=['room_items'])

        if selected_item == 'many':
            self.session.send_to_client(strings.many_found)
        elif selected_item is None:
            self.session.send_to_client(strings.not_found)
        elif selected_item.visible != 'takable':
            self.session.send_to_client(_('{item_name}: You can\'t take that item.').format(item_name=selected_item.name))
        else:
            self.session.user.get_current_world_inventory().add_item(selected_item)
            selected_item.remove_from_room()
            self.session.send_to_client(_('You took {item_name}.').format(item_name=selected_item.name))
        
        self.finish_interaction()


class Drop(Verb):
    '''Drops a item from your inventory.
    usage:
        command item_name
    '''

    command = _('drop ')

    def process(self, message):

        partial_name = message[len(self.command):]
        selected_item = util.name_to_entity(self.session, partial_name, substr_match=['inventory'])

        if selected_item is None:
            self.session.send_to_client(_('You don\'t have that item.'))
        elif selected_item == "many":
            self.session.send_to_client(_('There are more than one item with a similar name in your inventory. Be more specific.'))
        else:
            self.session.user.get_current_world_inventory().remove_item(selected_item)
            selected_item.put_in_room(self.session.user.room)
            self.session.send_to_client(_('You dropped {item_name}.').format(item_name=selected_item.name))
        
        self.finish_interaction()


class Inventory(Verb):
    '''Shows what you have in your inventory'''

    command = _('inventory')

    def process(self, message):
        if len(self.session.user.get_current_world_inventory().items) < 1:
            self.session.send_to_client(_('Your inventory is empty'))
        else:
            item_names = [item.name for item in self.session.user.get_current_world_inventory().items]
            item_list_items = [f'● {name}' for name in item_names]
            inventory_list = '\n'.join(item_list_items)
            self.session.send_to_client(_('You carry:\n{inventory_list}').format(inventory_list=inventory_list))

        self.finish_interaction()


class Give(Verb):
    command = _("give '")

    def process(self, message):
        message = message[len(self.command):]
        target_user_name, target_item_name = message.split("' ", 1)

        target_user = next(entities.User.objects(name=target_user_name, room=self.session.user.room, client_id__ne=None), None)
        item = next(entities.Item.objects(name=target_item_name, room=self.session.user.room, visible='takable'), None)

        if target_user is not None and item is not None:
            target_user.get_current_world_inventory().add_item(item)
            self.session.send_to_client(_('Done.'))
        else:
            self.session.send_to_client(_("The item/user is not in this room."))

        self.finish_interaction()

class TakeFrom(Verb):
    command = _("takefrom '")

    def process(self, message):
        message = message[len(self.command):]
        target_user_name, target_item_name = message.split("' ", 1)

        target_user = next(entities.User.objects(name=target_user_name, room=self.session.user.room, client_id__ne=None), None)
        
        if target_user is not None:
            target_item = next(filter(lambda i: i.name==target_item_name, target_user.get_current_world_inventory().items), None)
            if target_item is not None:
                target_user.get_current_world_inventory().remove_item(target_item)
                target_item.put_in_room(target_user.room)
                self.session.send_to_client(_('Done.'))
            else:
                self.session.send_to_client(_('The item is not in that user\'s inventory.'))
        else:
            self.session.send_to_client(_('That user is not here.'))

        self.finish_interaction()