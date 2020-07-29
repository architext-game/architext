"""This file defines all entities that exist within the game.
They are each defined as a mongoengine.Document, so that its values are automatically saved
and can be retrieved from mongodb database that server.py conects to on startup.

The responsibilities of each entity are:
  - Make its fields accesible from the database
  - Make the database handling trasparent (like calling the save() method at its own __init__)
  - Providing default values for non mandatory fields when they are needed, so they don't have to be setted manually.
  - Provide methods for controlled modification and deletion according to the entity behavior, so that methods dont have to be mannually touched and save() method called outside this module.
"""

import mongoengine


class Item(mongoengine.Document):
    name        = mongoengine.StringField(required=True)
    description = mongoengine.StringField(default='No tiene nada de especial.')
    visible     = mongoengine.BooleanField(default=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.save()


class World(mongoengine.Document):
    next_room_id = mongoengine.IntField(default=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.save()

    def get_unique_room_id(self):
        self.reload()
        id_to_serve = str(self.next_room_id)
        self.next_room_id = self.next_room_id + 1
        self.save()
        return id_to_serve

class Room(mongoengine.Document):
    name        = mongoengine.StringField(required=True)
    alias       = mongoengine.StringField(required=True, unique=True)  # unique id of the room, not shown to users
    description = mongoengine.StringField(default='')
    exits       = mongoengine.DictField()
    items       = mongoengine.ListField(mongoengine.ReferenceField(Item))

    def __init__(self, *args, **kwargs):
        if 'alias' in kwargs:
            super().__init__(*args, **kwargs)
        else:
            world = World.objects[0]
            default_alias = world.get_unique_room_id()
            super().__init__(alias=default_alias, *args, **kwargs)
        self.save()

    def _add_exit(self, exit, room_at_the_other_side):
        if exit in self.exits:
            raise Exception('Someone tried to create an exit with a duplicated name')
            
        self.exits[exit] = room_at_the_other_side
        self.save()

    def create_adjacent_room(self, there_name, exit_from_here, exit_from_there, there_description=""):
        new_room = Room(name=there_name, description=there_description, exits={exit_from_there: self})
        self._add_exit(exit_from_here, new_room)
        return new_room

    def add_item(self, item):
        self.items.append(item)
        self.save()

    def connect(self, exit_name, other_room):
        self.exits[exit_name]=other_room
        self.save()

class User(mongoengine.Document):
    name = mongoengine.StringField(required=True)
    room = mongoengine.ReferenceField(Room, required=True)
    client_id = mongoengine.IntField(default=None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.save()

    def move(self, exit):
        if exit in self.room.exits:
            self.room = self.room.exits[exit]
            self.save()

    def teleport(self, room):
        self.room = room
        self.save()

    def connect(self, client_id):
        self.client_id = client_id
        self.save()

    def disconnect(self):
        self.client_id = None
        self.save()
