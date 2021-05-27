import mongoengine
from . import item as item_module
from . import room as room_module

class Exit(mongoengine.Document):
    name = mongoengine.StringField(required=True)
    destination = mongoengine.ReferenceField('Room', required=True)
    description = mongoengine.StringField()
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
        return item_module.Item._get_name_validation_conditions(exit_name, local_room, ignore_item)

    @classmethod
    def name_is_valid(cls, exit_name, local_room, ignore_item=None):
        return item_module.Item.name_is_valid(exit_name, local_room, ignore_item)
    
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

    def clone(self, new_destination, new_room=None):
        new_exit = Exit(name=self.name, destination=new_destination, room=new_room, visible=self.visible, is_open=self.is_open, key_names=self.key_names.copy())
        return new_exit

    @classmethod
    def get_exits_in_world_state(cls, world_state):
        exits_in_world_state = []
        for room in room_module.Room.objects(world_state=world_state):
            exits_in_world_state += room.exits
        return exits_in_world_state