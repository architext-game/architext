import mongoengine
from .exceptions import *
from .. import util

class WorldSnapshot(mongoengine.Document):
    NAME_MAX_LENGTH = 36

    name = mongoengine.StringField(required=True)
    public = mongoengine.BooleanField(default=False)
    snapshoted_state = mongoengine.ReferenceField('WorldState', required=True)

    def __init__(self, *args, save_on_creation=True, **kwargs):
        super().__init__(*args, **kwargs)
        if self.id is None and save_on_creation:
                self.save()

    # called by mongoengine on save
    def clean(self):
        self.name = util.fix_string(self.name, max_length=self.NAME_MAX_LENGTH, remove_breaks=True)

    def publish(self):
        self.public = True
        self.save()

    def unpublish(self):
        self.public = False
        self.save()

    def delete(self):
        if self.public:
            raise CantDelete("Can't delete a public snapshot")
        self.snapshoted_state.delete()
        super().delete()