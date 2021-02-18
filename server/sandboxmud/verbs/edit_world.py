from . import verb

class EditWorld(verb.Verb):
    command = 'edit world'
    permissions = verb.PRIVILEGED

    def process(self, message):
        self.session.send_to_client('qué nuevo nombre quieres ponerle al mundo?')
        self.process = self.process_new_world_name

    def process_new_world_name(self, message):
        if not message:
            self.session.send_to_client("El nombre no puede estar vacío")
            return

        world = self.session.user.room.world_state.get_world()
        world.name = message
        world.save()
        self.finish_interaction()
        self.session.send_to_client("hecho")
        return