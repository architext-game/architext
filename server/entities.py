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

class CustomVerb(mongoengine.Document):
    name = mongoengine.StringField()
    commands = mongoengine.ListField(mongoengine.StringField())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.save()


class Item(mongoengine.Document):
    name        = mongoengine.StringField(required=True)
    description = mongoengine.StringField(default='No tiene nada de especial.')
    visible     = mongoengine.StringField(choices=['listed', 'hidden', 'obvious'], default='listed')
    custom_verbs = mongoengine.ListField(mongoengine.ReferenceField(CustomVerb))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.save()

    def obvious(self):
        return self.visible == 'obvious'
    
    def listed(self):
        return self.visible == 'listed'

    def hidden(self):
        return self.visible == 'hidden'

    def add_custom_verb(self, custom_verb):
        self.custom_verbs.append(custom_verb)
        self.save()


class World(mongoengine.Document):
    next_room_id = mongoengine.IntField(default=0)
    custom_verbs = mongoengine.ListField(mongoengine.ReferenceField(CustomVerb))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.save()

    def get_unique_room_id(self):
        self.reload()
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.save()

    def obvious(self):
        return self.visible == 'obvious'
    
    def listed(self):
        return self.visible == 'listed'

    def hidden(self):
        return self.visible == 'hidden'
        

class Room(mongoengine.Document):
    name        = mongoengine.StringField(required=True)
    alias       = mongoengine.StringField(required=True, unique=True)  # unique id of the room, not shown to users
    description = mongoengine.StringField(default='')
    exits       = mongoengine.ListField(mongoengine.ReferenceField('Exit', reverse_delete_rule=mongoengine.PULL))  # deleted exits are auto-removed from the list
    items       = mongoengine.ListField(mongoengine.ReferenceField(Item))
    custom_verbs = mongoengine.ListField(mongoengine.ReferenceField(CustomVerb))

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
        self.items.append(item)
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
    room = mongoengine.ReferenceField(Room, required=True)
    client_id = mongoengine.IntField(default=None)
    master_mode = mongoengine.BooleanField(default=False)

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


