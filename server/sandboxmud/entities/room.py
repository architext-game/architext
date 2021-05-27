import mongoengine
from . import exit as exit_module
from . import item as item_module
from . import user as user_module

class Room(mongoengine.Document):
    name        = mongoengine.StringField(required=True)
    world_state = mongoengine.ReferenceField('WorldState')
    alias       = mongoengine.StringField(required=True)  # id of the room, unique in each world state
    description = mongoengine.StringField()
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

    def get_exit(self, exit_name=None, destination=None):
        if exit_name is not None and destination is not None:
            return next(exit_module.Exit.objects(room=self, name=exit_name, destination=destination), None)
        if exit_name is not None:
            return next(exit_module.Exit.objects(room=self, name=exit_name), None)
        if destination is not None:
            return next(exit_module.Exit.objects(room=self, destination=destination), None)
        return None

    @property
    def items(self):
        if self.id is None:  # if the room is not yet saved into db it cannot have any items
            return []
        return list(item_module.Item.objects(room=self))

    @property
    def exits(self):
        if self.id is None:  # if the room is not yet saved into db it cannot have any items
            return []
        return list(exit_module.Exit.objects(room=self))

    @property
    def users(self):
        if self.id is None:  # if the room is not yet saved into db it cannot have any items
            return []
        return list(user_module.User.objects(room=self))

    def clone(self, new_world_state=None):
        new_room = Room(name=self.name, alias=self.alias, description=self.description, world_state=new_world_state)
        new_custom_verbs = []
        for custom_verb in self.custom_verbs:
            new_custom_verbs.append(custom_verb.clone())
        new_room.custom_verbs = new_custom_verbs
        for item in self.items:
            item.clone(new_room=new_room)
        new_room.save()
        return new_room

    def delete(self):
        for custom_verb in self.custom_verbs:
            custom_verb.delete()
        super().delete()