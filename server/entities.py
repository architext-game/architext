import mongoengine

class Item(mongoengine.Document):
    name        = mongoengine.StringField(required=True)
    description = mongoengine.StringField()
    visible     = mongoengine.BooleanField(default=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.save()


class World(mongoengine.Document):
    next_room_id = mongoengine.IntField(required=True, default=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.save()

class Room(mongoengine.Document):
    # mongoengine fields
    name        = mongoengine.StringField(required=True)
    description = mongoengine.StringField()
    exits       = mongoengine.DictField()
    items       = mongoengine.ListField(mongoengine.ReferenceField(Item))
    alias       = mongoengine.StringField(unique=True)

    def __init__(self, *args, **kwargs):
        if 'alias' in kwargs:
            super().__init__(*args, **kwargs)
        else:
            world = World.objects[0]
            default_alias = str(world.next_room_id)
            super().__init__(alias=default_alias, *args, **kwargs)
            world.next_room_id = world.next_room_id + 1
            world.save()
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
    client_id = mongoengine.IntField()

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
