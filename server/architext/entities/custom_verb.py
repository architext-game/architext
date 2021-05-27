import mongoengine

class CustomVerb(mongoengine.Document):
    names = mongoengine.ListField(mongoengine.StringField())
    commands = mongoengine.ListField(mongoengine.StringField())

    def __init__(self, *args, save_on_creation=True, **kwargs):
        super().__init__(*args, **kwargs)
        if self.id is None and save_on_creation:
            self.save()

    def is_name(self, verb_name):
        return verb_name in self.names

    def clone(self):
        new_custom_verb = CustomVerb(names=self.names.copy(), commands=self.commands.copy())
        new_custom_verb.save()
        return new_custom_verb