from .verb import Verb
import entities

class DeleteRoom(Verb):
    command = 'eliminarsala'

    def process(self, message):
        room_to_delete = self.session.user.room
        room_to_delete.reload()

        if len([user for user in entities.User.objects(room=room_to_delete) if user.client_id != None]) > 1:
            self.session.send_to_client("No puedes borrar la sala si hay mas gente conectada aquí.")
        if room_to_delete.alias == "0":
            self.session.send_to_client('No puedes eliminar la sala inicial. Prueba a editarla si no te gusta :-)')
        else:
            connected_rooms = room_to_delete.exits.values()

            for connected_room in connected_rooms:
                exits_to_pop = []
                for exit_there, destination in connected_room.exits.items():
                    if destination == room_to_delete:
                        exits_to_pop.append(exit_there)
                for exit_to_pop in exits_to_pop:
                    connected_room.exits.pop(exit_to_pop)
                if exits_to_pop:
                    connected_room.save()
            
            for item in room_to_delete.items:
                item.delete()

            room_to_escape_from_oblivion = entities.Room.objects.first()
            self.session.user.teleport(room_to_escape_from_oblivion)
            for user in entities.User.objects(room=room_to_delete):
                user.teleport(room_to_escape_from_oblivion)

            room_to_delete.delete()
            self.session.send_to_client("Sala eliminada. Espero que no hayas dejado muchas salas desconectadas.")
            
        self.finished = True

class DeleteExit(Verb):
    command = 'eliminarsalida '

    def process(self, message):
        command_length = len(self.command)
        exit = message[command_length:]

        if exit in self.session.user.room.exits.keys():
            self.delete_exit(exit)
            self.session.send_to_client("Borrada.")
        else:
            self.session.send_to_client("No existe esa salida.")

        self.finished = True

    def delete_exit(self, exit_here):
        this_room = self.session.user.room
        other_room = self.session.user.room.exits[exit_here]
        
        this_room.exits.pop(exit_here)

        for exit_there, room in other_room.exits.items():
            if room == this_room:
                other_room.exits.pop(exit_there)
                break
        
        this_room.save()
        other_room.save()

class DeleteItem(Verb):
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
        self.finished = True

