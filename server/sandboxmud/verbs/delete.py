from . import verb
from .. import entities

class DeleteRoom(verb.Verb):
    """This verb allows users to delete their current room.
    A room where there are other connected players cannot be deleted.
    Also, the initial room (with alias 0) cannot be deleted.
    Note that rooms may be left disconnected after the use of this command"""

    command = 'eliminarsala'
    permissions = verb.PRIVILEGED

    def process(self, message):
        room_to_delete = self.session.user.room

        if len([user for user in entities.User.objects(room=room_to_delete) if user.client_id != None]) > 1:
            self.session.send_to_client("No puedes borrar la sala si hay mas gente conectada aquí.")
        if room_to_delete.alias == "0":
            self.session.send_to_client('No puedes eliminar la sala inicial. Prueba a editarla si no te gusta :-)')
        else:
            # exits connecting to this room are implicitly removed from db and from exit lists in all rooms, due to its definition in entities.py

            for item in room_to_delete.items:
                item.delete()

            for exit in room_to_delete.exits:
                exit.delete()

            room_to_escape_from_oblivion = entities.Room.objects.first()
            self.session.user.teleport(room_to_escape_from_oblivion)
            for user in entities.User.objects(room=room_to_delete):
                user.teleport(room_to_escape_from_oblivion)

            room_to_delete.delete()
            self.session.send_to_client("Sala eliminada. Espero que no hayas dejado muchas salas desconectadas.")
            
        self.finish_interaction()

class DeleteExit(verb.Verb):
    """With this verb users can delete an exit of their current room. Since (for now) exits are allways two-way, it also
    deletes the exit from the other room"""

    command = 'eliminarsalida '
    permissions = verb.PRIVILEGED

    def process(self, message):
        command_length = len(self.command)
        exit_name = message[command_length:]

        if exit_name in [exit.name for exit in self.session.user.room.exits]:
            exit = self.session.user.room.get_exit(exit_name=exit_name)
            destination = exit.destination
            exit_from_there = destination.get_exit(destination=self.session.user.room)
            warning = ''
            if exit_from_there is not None:
                warning = f'\n {chr(10060)} La salida "{exit_from_there.name}" en "{destination.name}" que lleva hasta aquí no ha sido borrada (y puede que haya más).'
            self.session.send_to_client(f'Salida borrada: "{exit_name}"\n{chr(9472)*(17+len(exit_name))}\nEl destino era "{destination.name}" (alias: {destination.alias}){warning}')
            exit.delete()
        else:
            self.session.send_to_client(f'En esta sala no hay ninguna salida llamada "{exit_name}".\nRecuerda que para eliminar una salida debes escribir su nombre exacto.')

        self.finish_interaction()

    def delete_exit(self, exit_here_name):
        this_room = self.session.user.room
        other_room = self.session.user.room.get_exit(exit_here_name).destination
        
        exit = self.session.user.room.get_exit(exit_here_name).delete()
        # this_room.delete_exit(exit_here_name)
            

class DeleteItem(verb.Verb):
    """By using this verb users can delete items that are in their current room"""

    command = 'eliminarobjeto '
    permissions = verb.PRIVILEGED

    def process(self, message):
        command_length = len(self.command)
        item_name = message[command_length:]
        selected_item = next(entities.Item.objects(room=self.session.user.room, name=item_name), None)

        if selected_item is None:
            self.session.send_to_client(f"No hay un objeto llamado {item_name} en esta sala.\nRecuerda que para eliminarlo, debes escribir su nombre exacto.")
        else:
            selected_item.delete()
            self.session.send_to_client(f'Objeto "{item_name}" eliminado')
        self.finish_interaction()

