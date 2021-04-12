from . import verb

class EditWorld(verb.Verb):
    command = 'editarmundo'
    permissions = verb.PRIVILEGED

    def process(self, message):
        self.session.send_to_client(f'Editando el nombre del mundo\n{chr(9472)*29}\n{chr(10060)} Para cancelar, introduce "/".\n\nNuevo nombre:')
        self.process = self.process_new_world_name

    def process_new_world_name(self, message):
        if message == '/':
            self.session.send_to_client('Edición cancelada.')
            self.finish_interaction()
            return
        if not message:
            self.session.send_to_client("El nombre no puede estar vacío")
            return

        world = self.session.user.room.world_state.get_world()
        world.name = message
        world.save()
        self.finish_interaction()
        self.session.send_to_client("Nombre cambiado.")
        return