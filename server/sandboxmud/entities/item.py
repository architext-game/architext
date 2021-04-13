import mongoengine
from .exceptions import *
from . import exit as exit_module
from . import inventory as inventory_module
from . import room as room_module
import re

class Item(mongoengine.Document):
    item_id      = mongoengine.StringField(default=None)
    name         = mongoengine.StringField(required=True)
    description  = mongoengine.StringField(default='No tiene nada de especial.')
    visible      = mongoengine.StringField(choices=['listed', 'hidden', 'obvious', 'takable'], default='listed')
    custom_verbs = mongoengine.ListField(mongoengine.ReferenceField('CustomVerb'))
    room         = mongoengine.ReferenceField('Room', default=None)
    saved_in     = mongoengine.ReferenceField('WorldState', default=None)

    def __init__(self, *args, save_on_creation=True, **kwargs):
        super().__init__(*args, **kwargs)
        if self.id is None:  # if this is a newly created Item, instead of a pre-existing document being instantiated by mongoengine.
            if self.saved_in is not None and self.item_id is None:
                self.item_id = self._generate_item_id()
            if save_on_creation:
                self.save()

    def save(self):
        self.ensure_i_am_valid()
        super().save()

    def _generate_item_id(self):
        id_number = 1
        item_id = f"{self.name}#{id_number}"
        while len(Item.objects(item_id=item_id, saved_in=self.saved_in)) > 0:
            id_number = id_number + 1
            item_id = f"{self.name}#{id_number}"
        return item_id

    def ensure_i_am_valid(self):
        name_conditions = self._get_name_validation_conditions(self.name,  self.room, self, self.is_takable())
        for condition in name_conditions.values():
            if not condition['condition']:
                raise condition['exception']

    @classmethod
    def _get_name_validation_conditions(cls, item_name, local_room=None, ignore_item=None, takable=False):
        conditions_for_this_item = {}

        snapshot_conditions = {
            'name_is_not_empty': {
                'condition': len(item_name)>0,
                'exception': EmptyName()
            },
            'has_name_format': {
                'condition': not re.search("#\d+$", item_name),
                'exception': WrongNameFormat()
            }
        }        

        conditions_for_this_item = {**conditions_for_this_item, **snapshot_conditions}

        if local_room is not None:
            item_conditions = {
                'unique_in_room': {
                    'condition': item_name not in [item.name for item in local_room.items+local_room.exits if item != ignore_item],
                    'exception': RoomNameClash()
                },
                'there_is_no_takable_with_same_name': {
                    'condition': item_name not in [takable_item.name for takable_item in Item.get_items_in_world_state(local_room.world_state) if takable_item != ignore_item and takable_item.visible=='takable'],
                    'exception': TakableItemNameClash()
                }
            }
            conditions_for_this_item = {**conditions_for_this_item, **item_conditions}

        if local_room is not None and takable:
            takable_item_conditions = {
                'name_is_globally_unique': {
                    'condition': (
                            item_name not in [item.name for item in Item.get_items_in_world_state(local_room.world_state) if item != ignore_item]
                            and item_name not in [item.name for item in exit_module.Exit.get_exits_in_world_state(local_room.world_state) if item != ignore_item]
                        ),
                    'exception': NameNotGloballyUnique()
                }
            }
            conditions_for_this_item = {**conditions_for_this_item, **takable_item_conditions}

        return conditions_for_this_item

    @classmethod
    def name_is_valid(cls, item_name, local_room, ignore_item=None, takable=False):
        conditions = cls._get_name_validation_conditions(item_name, local_room, ignore_item, takable)
        for condition in conditions.values():
            if not condition['condition']:
                return False
        return True

    def is_obvious(self):
        return self.visible == 'obvious'
    
    def is_listed(self):
        return self.visible == 'listed' or self.visible == 'takable'

    def is_hidden(self):
        return self.visible == 'hidden'

    def is_takable(self):
        return self.visible == 'takable'

    def add_custom_verb(self, custom_verb):
        self.custom_verbs.append(custom_verb)
        self.save()

    def clone(self, new_room=None, new_saved_in=None, new_item_id=None):
        new_item = Item(name=self.name, description=self.description, visible=self.visible, room=new_room, saved_in=new_saved_in, item_id=new_item_id)
        for custom_verb in self.custom_verbs:
            new_item.add_custom_verb(custom_verb.clone())
        new_item.save()
        return new_item

    @classmethod
    def get_items_in_world_state(cls, world_state):
        items_at_rooms = []
        for room in room_module.Room.objects(world_state=world_state):
            items_at_rooms += room.items

        items_being_carried = []
        for inventory in inventory_module.Inventory.objects(world_state=world_state):
            items_being_carried += inventory.items

        return items_at_rooms + items_being_carried

    def put_in_room(self, room):
        self.room = room
        self.save()

    def remove_from_room(self):
        self.room = None
        self.save()

    def delete(self):
        for custom_verb in self.custom_verbs:
            custom_verb.delete()
        super().delete()