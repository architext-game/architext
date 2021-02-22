import mongoengine
from .exceptions import *
from . import user as user_module
from . import world_state as world_state_module

class World(mongoengine.Document):
    name = mongoengine.StringField(required=True)
    world_state = mongoengine.ReferenceField('WorldState', required=True)
    snapshots = mongoengine.ListField(mongoengine.ReferenceField('WorldSnapshot'))
    all_can_edit = mongoengine.BooleanField(default=False)
    editors = mongoengine.ListField(mongoengine.ReferenceField('User'))
    creator = mongoengine.ReferenceField('User', required=True)

    def __init__(self, *args, save_on_creation=True, **kwargs):
        super().__init__(*args, **kwargs)
        if self.id is None:
            if self.world_state is None:
                self.world_state = world_state_module.WorldState()
            if save_on_creation:
                self.save()

    def add_snapshot(self, snapshot):
        self.snapshots.append(snapshot)
        self.save()

    def is_creator(self, user):
        return user == self.creator

    def is_privileged(self, user):
        return self.is_creator(user) or user in self.editors

    def set_to_free_edition(self):
        self.all_can_edit = True
        self.save()

    def set_to_privileged_edition(self):
        self.all_can_edit = False
        self.save()

    def add_editor(self, user):
        if user not in self.editors:
            self.editors.append(user)
            self.save()

    def remove_editor(self, user):
        if user in self.editors:
            self.editors.remove(user)
            self.save()

    def get_connected_users(self):
        users = user_module.User.objects(client_id__ne=None, room__ne=None)
        return len(list(filter(lambda u: u.room.world_state==self.world_state, users)))

    def delete(self):
        for snapshot in self.snapshots:
            if snapshot.public:
                raise CantDelete("Can't delete a world that has one or more of its snapshots published.")
        for snapshot in self.snapshots:
            snapshot.delete()
        self.world_state.delete()
        super().delete()