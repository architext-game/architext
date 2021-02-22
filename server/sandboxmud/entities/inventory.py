import mongoengine

class Inventory(mongoengine.Document):
    user  = mongoengine.ReferenceField('User', required=True)
    world_state = mongoengine.ReferenceField('WorldState', required=True)
    items = mongoengine.ListField(mongoengine.ReferenceField('Item'))

    def __init__(self, *args, save_on_creation=True, **kwargs):
        super().__init__(*args, **kwargs)
        if self.id is None and save_on_creation:
                self.save()

    def add_item(self, item):
        item.remove_from_room()
        self.items.append(item)
        self.save()

    def remove_item(self, item):
        self.items.remove(item)
        self.save()

    def clone(self, new_world_state):
        new_inventory = Inventory(world_state=new_world_state, user=self.user)
        for item in self.items:
            new_inventory.items.append(item.clone())
        new_inventory.save()
        return new_inventory