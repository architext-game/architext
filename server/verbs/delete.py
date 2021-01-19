from .verb import Verb
import entities

class DeleteRoom(Verb):
    """This verb allows users to delete their current room.
    A room where there are other connected players cannot be deleted.
    Also, the initial room (with alias 0) cannot be deleted.
    Note that rooms may be left disconnected after the use of this command"""

    command = 'eliminarsala'

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

class DeleteExit(Verb):
    """With this verb users can delete an exit of their current room. Since (for now) exits are allways two-way, it also
    deletes the exit from the other room"""

    command = 'eliminarsalida '

    def process(self, message):
        command_length = len(self.command)
        exit_name = message[command_length:]

        if exit_name in [exit.name for exit in self.session.user.room.exits]:
            self.delete_exit(exit_name)
            self.session.send_to_client("Borrada la salida desde aquí hasta allí. Ojo, no he intentado borrar la salida desde allí hasta aquí. Si quieres hacerlo, vas para allá y lo haces desde allí.")
        else:
            self.session.send_to_client("No existe esa salida.")

        self.finish_interaction()

    def delete_exit(self, exit_here_name):
        this_room = self.session.user.room
        other_room = self.session.user.room.get_exit(exit_here_name).destination
        
        this_room.delete_exit(exit_here_name)
            

class DeleteItem(Verb):
    """By using this verb users can delete items that are in their current room"""

    command = 'eliminarobjeto '

    def process(self, message):
        command_length = len(self.command)
        message = message[command_length:]
        selected_item = None
        items = self.session.user.room.items
        for item in items:
            if item.name == message:
                selected_item = item
                break

        if selected_item is None:
            self.session.send_to_client("No está ese objeto.")
        else:
            self.session.user.room.items.remove(selected_item)
            self.session.user.room.save()
            selected_item.delete()
            self.session.send_to_client("Eliminado")
        self.finish_interaction()

