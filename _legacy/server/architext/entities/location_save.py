import mongoengine

class LocationSave(mongoengine.Document):
    user  = mongoengine.ReferenceField('User', required=True)
    world = mongoengine.ReferenceField('World', required=True)
    room  = mongoengine.ReferenceField('Room', required=True)

    def __init__(self, *args, save_on_creation=True, **kwargs):
        super().__init__(*args, **kwargs)
        if self.id is None and save_on_creation:
                self.save()

    def change_room(self, new_room):
        self.room = new_room
        self.save()