import mongoengine
from . import inventory as inventory_module
from . import location_save as location_save_module
from . import exceptions
from .. import util
from .. import entities

def validate_user_name(name):
    if '\n' in name:
        raise exceptions.ValueWithLineBreaks()
    elif len(name) > entities.User.NAME_MAX_LENGTH:
        raise exceptions.ValueTooLong()
    elif name == "":
        raise exceptions.EmptyName()

class User(mongoengine.Document):
    NAME_MAX_LENGTH = 26

    name = mongoengine.StringField(required=True, validation=validate_user_name)
    room = mongoengine.ReferenceField('Room')
    client_id = mongoengine.IntField(default=None)
    master_mode = mongoengine.BooleanField(default=False)
    joined_worlds = mongoengine.ListField(mongoengine.ReferenceField('World'))

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

    def get_location_save(self, world):
        return next(location_save_module.LocationSave.objects(user=self, world=world), None)

    def enter_world(self, world):
        location_save = self.get_location_save(world)
        if location_save is not None and location_save.room.world_state == world.world_state:
            self.room = location_save.room
        else:
            self.room = world.world_state.starting_room
        if world not in self.joined_worlds:
            self.joined_worlds.append(world)
        self.save()

    def leave_world(self):
        if self.room is not None:
            current_world = self.room.world_state.get_world()
            location_save = self.get_location_save(current_world)
            if location_save is not None:
                location_save.change_room(self.room)
            else:
                location_save_module.LocationSave(user=self, world=self.room.world_state.get_world(), room=self.room)
        self.room = None
        self.save()

    def save_item(self, item):
        item_snapshot = item.clone()
        item_snapshot.saved_in = self.room.world_state
        item_snapshot.item_id = item_snapshot._generate_item_id()
        item_snapshot.save()
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
        inventory = next(inventory_module.Inventory.objects(user=self, world_state=world_state), None)
        if inventory is None:
            inventory = inventory_module.Inventory(user=self, world_state=world_state)
        return inventory

    def get_current_world_inventory(self):
        return self.get_inventory_from(self.room.world_state)
