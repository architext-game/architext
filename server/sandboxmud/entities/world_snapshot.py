import mongoengine
from .exceptions import *

class WorldSnapshot(mongoengine.Document):
    name = mongoengine.StringField(required=True)
    public = mongoengine.BooleanField(default=False)
    snapshoted_state = mongoengine.ReferenceField('WorldState', required=True)

    def __init__(self, *args, save_on_creation=True, **kwargs):
        super().__init__(*args, **kwargs)
        if self.id is None and save_on_creation:
                self.save()

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