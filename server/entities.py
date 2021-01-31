"""This file defines all entities that exist within the game.
They are each defined as a mongoengine. Document, so each instance of any of these classes
represents a particular document in our MongoDB database. Multiple instances of the same
document may be present at the same time. Thus, Entities should be treated with
care in order to avoid possible inconsistencies. We should call the reload()
method of each entity instance we have created prior to a possible change made from elsewere.
In particular, this happens whenever a session gets a new message to process. At this point,
other sessions may have altered the state of the world that the session knew. So the session
must call reload() on every entity instance they reference.
Also, we must ensure that every change to the state of an entity instance is saved to database.
For that, we use the save() method. Every method of an entity that alters their state must include
a call to self.save() after all the changes are made. When any change is made to the entity without
the use of its own methods, save() must be called on the entity.

The responsibilities of each entity are:
  - Make its fields accesible from the database
  - Make the database handling trasparent (like calling the save() method at its own __init__)
  - Providing default values for non mandatory fields when they are needed, so they don't have to be setted manually.
  - Provide methods for controlled modification and deletion according to the entity behavior, so that methods dont have to be mannually touched and save() method called outside this module.
"""

import mongoengine
import entities
import re

class CustomVerb(mongoengine.Document):
    names = mongoengine.ListField(mongoengine.StringField())
    commands = mongoengine.ListField(mongoengine.StringField())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.save()

    def is_name(self, verb_name):
        return verb_name in self.names

    def clone(self):
        new_custom_verb = CustomVerb(names=self.names.copy(), commands=self.commands.copy())
        new_custom_verb.save()
        return new_custom_verb


class Item(mongoengine.Document):
    item_id      = mongoengine.StringField(unique=True, required=True)
    name         = mongoengine.StringField(required=True)
    description  = mongoengine.StringField(default='No tiene nada de especial.')
    visible      = mongoengine.StringField(choices=['listed', 'hidden', 'obvious', 'takable'], default='listed')
    custom_verbs = mongoengine.ListField(mongoengine.ReferenceField('CustomVerb'))
    room         = mongoengine.ReferenceField('Room', default=None)

    def __init__(self, *args, save_on_creation=True, **kwargs):
        super().__init__(*args, **kwargs)
        if self.id is None:  # if this is a newly created Item, instead of a pre-existing document being instantiated by mongoengine.
            self.item_id = self.generate_item_id()
            if save_on_creation:
                self.save()

    def save(self):
        self.ensure_i_am_valid()
        super().save()

    def generate_item_id(self):
        id_number = 1
        item_id = "{}#{}".format(self.name, id_number)
        while len(entities.Item.objects(item_id=item_id)) > 0:
            id_number = id_number + 1
            item_id = "{}#{}".format(self.name, id_number)
        return item_id

    def ensure_i_am_valid(self):
        name_conditions = self.get_name_validation_conditions(self.name,  self.room, self, self.is_takable())
        for condition in name_conditions.values():
            if not condition['condition']:
                raise condition['exception']

    @classmethod
    def get_name_validation_conditions(cls, item_name, local_room=None, ignore_item=None, takable=False):
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
                    'condition': item_name not in [takable_item.name for takable_item in entities.Item.get_items_in_world() if takable_item != ignore_item and takable_item.visible=='takable'],
                    'exception': TakableItemNameClash()
                }
            }
            conditions_for_this_item = {**conditions_for_this_item, **item_conditions}

        if local_room is not None and takable:
            takable_item_conditions = {
                'name_is_globally_unique': {
                    'condition': (
                            item_name not in [item.name for item in entities.Item.get_items_in_world() if item != ignore_item]
                            and item_name not in [item.name for item in entities.Exit.get_exits_in_world() if item != ignore_item]
                        ),
                    'exception': NameNotGloballyUnique()
                }
            }
            conditions_for_this_item = {**conditions_for_this_item, **takable_item_conditions}

        return conditions_for_this_item

    @classmethod
    def name_is_valid(cls, item_name, local_room, ignore_item=None, takable=False):
        conditions = cls.get_name_validation_conditions(item_name, local_room, ignore_item, takable)
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

    def clone(self):
        new_item = Item(name=self.name, description=self.description, visible=self.visible)
        for custom_verb in self.custom_verbs:
            new_item.add_custom_verb(custom_verb.clone())
        new_item.save()
        return new_item

    @classmethod
    def get_items_in_world(cls):
        return cls.objects(room__ne=None)


class World(mongoengine.Document):
    next_room_id = mongoengine.IntField(default=0)
    custom_verbs = mongoengine.ListField(mongoengine.ReferenceField('CustomVerb'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.save()

    def get_unique_room_id(self):
        id_to_serve = str(self.next_room_id)
        self.next_room_id = self.next_room_id + 1
        self.save()
        return id_to_serve

    def add_custom_verb(self, custom_verb):
        self.custom_verbs.append(custom_verb)
        self.save()

class Exit(mongoengine.Document):
    name = mongoengine.StringField(required=True)
    destination = mongoengine.ReferenceField('Room', required=True)  # reverse delete rule specified later due to circular rule
    description = mongoengine.StringField(default='No tiene nada de especial.')
    visible = mongoengine.StringField(choices=['listed', 'hidden', 'obvious'], default='listed')
    is_open = mongoengine.BooleanField(default=True)
    key_names = mongoengine.ListField(mongoengine.StringField())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.save()

    @classmethod
    def check_exit_name(cls, exit_name, local_room, ignore_item=None):
        Item.check_item_name(cls, exit_name, local_room, ignore_item, takable=False)

    def is_obvious(self):
        return self.visible == 'obvious'
    
    def add_key(self, item_name):
        self.key_names.append(item_name)
        self.save()

    def remove_key(self, item_name):
        self.key_names.remove(item_name)
        self.save()

    def open(self):
        self.is_open = True
        self.save()

    def close(self):
        self.is_open = False
        self.save()

    def is_listed(self):
        return self.visible == 'listed'

    def is_hidden(self):
        return self.visible == 'hidden'

    @classmethod
    def get_exits_in_world(cls):
        return cls.objects()
        

class Room(mongoengine.Document):
    name        = mongoengine.StringField(required=True)
    alias       = mongoengine.StringField(required=True, unique=True)  # unique id of the room, not shown to users
    description = mongoengine.StringField(default='')
    exits       = mongoengine.ListField(mongoengine.ReferenceField('Exit', reverse_delete_rule=mongoengine.PULL))  # deleted exits are auto-removed from the list
    items       = mongoengine.ListField(mongoengine.ReferenceField('Item'))
    custom_verbs = mongoengine.ListField(mongoengine.ReferenceField('CustomVerb'))

    def __init__(self, *args, **kwargs):
        if 'alias' in kwargs:
            super().__init__(*args, **kwargs)
        else:
            world = World.objects[0]
            default_alias = world.get_unique_room_id()
            super().__init__(alias=default_alias, *args, **kwargs)
        self.save()

    def add_exit(self, exit_name, destination):
        if exit_name in [exit.name for exit in self.exits]:
            raise Exception('Someone tried to create an exit with a duplicated name')
        
        new_exit = Exit(name=exit_name, destination=destination)
        self.exits.append(new_exit)
        self.save()

    def delete_exit(self, exit_name):
        exit_to_delete = self.get_exit(exit_name)
        self.exits.remove(exit_to_delete)
        self.save()

    def get_exit(self, exit_name):
        return next(filter(lambda x: x.name==exit_name, self.exits))

    def create_adjacent_room(self, there_name, exit_from_here, exit_from_there, there_description=""):
        new_room = Room(name=there_name, description=there_description)
        new_room.add_exit(exit_name=exit_from_there, destination=self)
        self.add_exit(exit_from_here, new_room)
        return new_room

    def add_item(self, item):
        item.room = self
        item.save()
        self.items.append(item)
        self.save()

    def remove_item(self, item):
        item.room = None
        item.save()
        self.items.remove(item)
        self.save()

    def add_custom_verb(self, custom_verb):
        self.custom_verbs.append(custom_verb)
        self.save()

# make exits pointing to a deleted room to be deleted as well
# can't specify it at class declaration because there is a circular delete rule:
# deleted exits are removed from list of exits in a room
Room.register_delete_rule(Exit, 'destination', mongoengine.CASCADE)


class User(mongoengine.Document):
    name = mongoengine.StringField(required=True)
    room = mongoengine.ReferenceField('Room', required=True)
    client_id = mongoengine.IntField(default=None)
    inventory = mongoengine.ListField(mongoengine.ReferenceField('Item'))
    master_mode = mongoengine.BooleanField(default=False)
    saved_items = mongoengine.ListField(mongoengine.ReferenceField('Item'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.save()

    def move(self, exit_name):
        if exit_name in [exit.name for exit in self.room.exits]:
            self.room = self.room.get_exit(exit_name).destination
            self.save()

    def teleport(self, room):
        self.room = room
        self.save()

    def add_item_to_inventory(self, item):
        self.inventory.append(item)
        self.save()

    def remove_item_from_inventory(self, item):
        self.inventory.remove(item)
        self.save()

    def save_item(self, item):
        item_snapshot = item.clone()
        self.saved_items.append(item_snapshot)
        self.save()
        return item_snapshot

    def connect(self, client_id):
        self.client_id = client_id
        self.save()

    def disconnect(self):
        self.client_id = None
        self.save()

    def enter_master_mode(self):
        self.master_mode = True
        self.save()

    def leave_master_mode(self):
        self.master_mode = False
        self.save()


class BadItem(Exception):
    """Raised when saving an item that does not abide by the item prerequisites"""

class EmptyName(BadItem):
    """Raised when creating an item with an empty name"""

class WrongNameFormat(BadItem):
    """Raised when creating an item with a bad formatted name"""

class RoomNameClash(BadItem):
    """Raised when creating an item with the same name of an exit at the
    same room"""

class TakableItemNameClash(BadItem):
    """Raised when creating an Item or Room that may be unique in their room,
    but may cause problems in other ways. e.g. if there is a takable item with
    that name somewhere else"""

class NameNotGloballyUnique(BadItem):
    """Raised when creating a takable item whose name is already present
    it any item or exit of the world."""