from . import verb
import textwrap
from .. import entities

class EditWorld(verb.Verb):
    command = 'editarmundo'
    permissions = verb.PRIVILEGED

    def __init__(self, session):
        super().__init__(session)
        self.world = self.session.user.room.world_state.get_world()
        self.option_number = None
        self.current_process_function = self.process_first_message


    def process(self, message):
        if message == '/':
            self.session.send_to_client("Edición cancelada.")
            self.finish_interaction()
        else:
            self.current_process_function(message)

    def process_first_message(self, message):
        # self.session.send_to_client(f'Editando el nombre del mundo\n{chr(9472)*29}\n{chr(10060)} Para cancelar, introduce "/".\n\nNuevo nombre:')
        out_message = textwrap.dedent(f"""
            Editando el mundo "{self.world.name}"
            {chr(9472)*(20+len(self.world.name))}
            {chr(10060)} Para cancelar, introduce '/' en cualquier momento.
            
            ¿Qué quieres cambiar? (introduce el número correspondiente)
             0 - Nombre
             1 - Cambiar público/privado"""
        )
        self.session.send_to_client(out_message)
        self.current_process_function = self.process_option_number

    def process_option_number(self, message):
        try:
            message = int(message)
        except ValueError:
            self.session.send_to_client('Debes introducir un número.')
            return
        
        options = {
            0: {
                "out_message": 'Introduce el nuevo valor para el nombre del mundo.',
                "next_process_function": self.process_new_world_name,
            },
            1: {
                "out_message": textwrap.dedent(f"""
                    Actualmente el mundo es {'público' if self.world.public else 'privado'}'
                    ¿Quieres cambiarlo a {'público' if not self.world.public else 'privado'}? [sí/no]"""
                ), 
                "next_process_function": self.process_public_choice,
            },
        }

        try:
            chosen_option = options[message]
        except KeyError:
            self.session.send_to_client('Introduce el número correspondiente a una de las opciones')
            return

        self.session.send_to_client(chosen_option["out_message"])
        self.current_process_function = chosen_option["next_process_function"]

    def process_new_world_name(self, message):
        if not message:
            self.session.send_to_client("El nombre no puede estar vacío")
            return

        world = self.session.user.room.world_state.get_world()
        world.name = message
        world.save()
        self.finish_interaction()
        self.session.send_to_client("Nombre cambiado.")
        return

    def process_public_choice(self, message):
        yes = ['si', 'sí', 'Si', 'Sí', 's', 'S']
        no  = ['no', 'No', 'n', 'N']

        if message in yes:
            try:
                self.world.toggle_public()
            except entities.PublicWorldLimitReached:
                self.session.send_to_client('Ya has llegado al límite de mundos públicos en este servidor. Haz privado otro mundo o pide al administrador que incremente tu límite.')
                self.finish_interaction()
                return
            self.session.send_to_client(f'Ahora el mundo es {"público" if self.world.public else "privado"}.')
            self.finish_interaction()
        elif message in no:
            self.session.send_to_client(f'OK. El mundo sigue siendo {"público" if self.world.public else "privado"}.')
            self.finish_interaction()
        else:
            self.session.send_to_client('Introduce "si" o "no".')