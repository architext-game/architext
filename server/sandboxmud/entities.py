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
import re


class CustomVerb(mongoengine.Document):
    names = mongoengine.ListField(mongoengine.StringField())
    commands = mongoengine.ListField(mongoengine.StringField())

    def __init__(self, *args, save_on_creation=True, **kwargs):
        super().__init__(*args, **kwargs)
        if self.id is None and save_on_creation:
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
            self.item_id = self._generate_item_id()
            if save_on_creation:
                self.save()

    def save(self):
        self.ensure_i_am_valid()
        super().save()

    def _generate_item_id(self):
        id_number = 1
        item_id = "{}#{}".format(self.name, id_number)
        while len(Item.objects(item_id=item_id)) > 0:
            id_number = id_number + 1
            item_id = "{}#{}".format(self.name, id_number)
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
                            and item_name not in [item.name for item in Exit.get_exits_in_world_state(local_room.world_state) if item != ignore_item]
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

    def clone(self):
        new_item = Item(name=self.name, description=self.description, visible=self.visible)
        for custom_verb in self.custom_verbs:
            new_item.add_custom_verb(custom_verb.clone())
        new_item.save()
        return new_item

    @classmethod
    def get_items_in_world_state(cls, world_state):
        items_at_rooms = []
        for room in Room.objects(world_state=world_state):
            items_at_rooms += room.items

        items_being_carried = []
        for inventory in Inventory.objects(world_state=world_state):
            items_being_carried += inventory.items

        return items_at_rooms + items_being_carried

    def put_in_room(self, room):
        self.room = room
        self.save()

    def remove_from_room(self):
        self.room = None
        self.save()

class World(mongoengine.Document):
    name = mongoengine.StringField(required=True)
    world_state = mongoengine.ReferenceField('WorldState', required=True)
    snapshots = mongoengine.ListField(mongoengine.ReferenceField('WorldSnapshot'))

    def __init__(self, *args, save_on_creation=True, **kwargs):
        super().__init__(*args, **kwargs)
        if self.id is None:
            if self.world_state is None:
                self.world_state = WorldState()
            if save_on_creation:
                self.save()

class WorldState(mongoengine.Document):
    starting_room = mongoengine.ReferenceField('Room', required=True)
    custom_verbs = mongoengine.ListField(mongoengine.ReferenceField('CustomVerb'))
    _next_room_id = mongoengine.IntField(default=1)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.id is None:
            if self.starting_room is None:
                self.starting_room = Room(alias='0', name='El Inicio', description='Esta sala es donde nacen los novatos. A partir de aquí se abren las puertas a diferentes mundos. Si no sabes moverte, escribe "ayuda" y descubrirás todo lo que puedes hacer.')
            if self.starting_room.alias != '0':
                raise Exception('The alias of a starting room must be "0"')
            self.starting_room.world_state = self
            self.save()
            self.starting_room.save()

    def get_unique_room_id(self):
        id_to_serve = str(self._next_room_id)
        self._next_room_id = self._next_room_id + 1
        self.save()
        return id_to_serve

    def add_custom_verb(self, custom_verb):
        self.custom_verbs.append(custom_verb)
        self.save()

class WorldSnapshot(mongoengine.Document):
    name = mongoengine.StringField(required=True)
    snapshoted_state = mongoengine.ReferenceField('WorldState')

class Inventory(mongoengine.Document):
    user  = mongoengine.ReferenceField('User', required=True)
    world_state = mongoengine.ReferenceField('WorldState', required=True)
    items = mongoengine.ListField(mongoengine.ReferenceField('Item'))

    def add_item(self, item):
        self.items.append(item)
        self.save()

    def remove_item(self, item):
        self.items.remove(item)
        self.save()

class Exit(mongoengine.Document):
    name = mongoengine.StringField(required=True)
    destination = mongoengine.ReferenceField('Room', required=True)
    description = mongoengine.StringField(default='No tiene nada de especial.')
    visible = mongoengine.StringField(choices=['listed', 'hidden', 'obvious'], default='listed')
    is_open = mongoengine.BooleanField(default=True)
    key_names = mongoengine.ListField(mongoengine.StringField())
    room = mongoengine.ReferenceField('Room', default=None)

    def __init__(self, *args, save_on_creation=True, **kwargs):
        super().__init__(*args, **kwargs)
        if self.id is None and save_on_creation:
            self.save()

    def save(self):
        self.ensure_i_am_valid()
        super().save()

    def ensure_i_am_valid(self):
        name_conditions = self._get_name_validation_conditions(self.name,  self.room, self)
        for condition in name_conditions.values():
            if not condition['condition']:
                raise condition['exception']

    @classmethod
    def _get_name_validation_conditions(cls, exit_name, local_room, ignore_item=None):
        return Item._get_name_validation_conditions(exit_name, local_room, ignore_item)

    @classmethod
    def name_is_valid(cls, exit_name, local_room, ignore_item=None):
        return Item.name_is_valid(exit_name, local_room, ignore_item)
    
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

    def is_obvious(self):
        return self.visible == 'obvious'

    def is_listed(self):
        return self.visible == 'listed'

    def is_hidden(self):
        return self.visible == 'hidden'

    @classmethod
    def get_exits_in_world_state(cls, world_state):
        exits_in_world_state = []
        for room in Room.objects(world_state=world_state):
            exits_in_world_state += room.exits
        return exits_in_world_state
        

class Room(mongoengine.Document):
    name        = mongoengine.StringField(required=True)
    world_state = mongoengine.ReferenceField('WorldState')
    alias       = mongoengine.StringField(required=True)  # id of the room, unique in each world state
    description = mongoengine.StringField(default='')
    custom_verbs = mongoengine.ListField(mongoengine.ReferenceField('CustomVerb'))

    def __init__(self, *args, save_on_creation=True, **kwargs):
        if 'alias' in kwargs:
            super().__init__(*args, **kwargs)
        else:
            default_alias = kwargs['world_state'].get_unique_room_id()
            super().__init__(alias=default_alias, *args, **kwargs)
        if self.id is None and save_on_creation:
            self.save()

    def add_custom_verb(self, custom_verb):
        self.custom_verbs.append(custom_verb)
        self.save()

    def get_exit(self, exit_name):
        return next(Exit.objects(room=self, name=exit_name), None)

    @property
    def items(self):
        if self.id is None:  # if the room is not yet saved into db it cannot have any items
            return []
        return list(Item.objects(room=self))

    @property
    def exits(self):
        if self.id is None:  # if the room is not yet saved into db it cannot have any items
            return []
        return list(Exit.objects(room=self))


class User(mongoengine.Document):
    name = mongoengine.StringField(required=True)
    room = mongoengine.ReferenceField('Room')
    client_id = mongoengine.IntField(default=None)
    master_mode = mongoengine.BooleanField(default=False)
    saved_items = mongoengine.ListField(mongoengine.ReferenceField('Item'))

    def __init__(self, *args, save_on_creation=True,  **kwargs):
        super().__init__(*args, **kwargs)
        if self.id is None and save_on_creation:
            self.save()

    def move(self, exit_name):
        if exit_name in [exit.name for exit in self.room.exits]:
            self.room = self.room.get_exit(exit_name).destination
            self.save()

    def teleport(self, room):
        self.room = room
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

    def get_inventory_from(self, world_state):
        inventory = next(Inventory.objects(user=self, world_state=world_state), None)
        if inventory is None:
            inventory = Inventory(user=self, world_state=world_state)
        return inventory

    def get_current_world_inventory(self):
        return self.get_inventory_from(self.room.world_state)


# delete rules
# example:
#   Entity1.register_delete_rule(Entity2, 'reference_field', delete_rule) 
# means:
#   when a document of type Entity1 is deleted, delete_rule happens to all Entity2 that referenced that Entity1 on its field 'referencefield'
# Note: rules are only applied to database, not runtime instances. They must be reloaded.
CustomVerb.register_delete_rule(Room, 'custom_verbs', mongoengine.PULL)
CustomVerb.register_delete_rule(Item, 'custom_verbs', mongoengine.PULL)
CustomVerb.register_delete_rule(WorldState, 'custom_verbs', mongoengine.PULL)
Item.register_delete_rule(Inventory, 'items', mongoengine.PULL)
Item.register_delete_rule(User, 'saved_items', mongoengine.DENY)
Room.register_delete_rule(User, 'room', mongoengine.DENY)
Room.register_delete_rule(Item, 'room', mongoengine.CASCADE)
Room.register_delete_rule(Exit, 'room', mongoengine.CASCADE)
Room.register_delete_rule(Exit, 'destination', mongoengine.CASCADE)
Room.register_delete_rule(WorldState, 'starting_room', mongoengine.DENY)
WorldState.register_delete_rule(Room, 'world_state', mongoengine.CASCADE) 
WorldState.register_delete_rule(Inventory, 'world_state', mongoengine.CASCADE)
WorldState.register_delete_rule(WorldSnapshot, 'snapshoted_state', mongoengine.CASCADE)
WorldSnapshot.register_delete_rule(World, 'snapshots', mongoengine.PULL)



# Exceptions related to entities
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