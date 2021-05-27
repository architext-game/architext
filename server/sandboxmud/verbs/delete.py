from . import verb
from .. import entities

class DeleteRoom(verb.Verb):
    """This verb allows users to delete their current room.
    A room where there are other connected players cannot be deleted.
    Also, the initial room (with alias 0) cannot be deleted.
    Note that rooms may be left disconnected after the use of this command"""

    command = _('deleteroom')
    permissions = verb.PRIVILEGED

    def process(self, message):
        room_to_delete = self.session.user.room

        if len([user for user in entities.User.objects(room=room_to_delete) if user.client_id != None]) > 1:
            self.session.send_to_client(_("You can't delete the room if there are other players here."))
        if room_to_delete.alias == "0":
            self.session.send_to_client(_('You can\'t delete the starting room. But you can edit it if you don\'t like it :-)'))
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
            self.session.send_to_client(_("The room and the exits leading to it have been deleted."))
            
        self.finish_interaction()

class DeleteExit(verb.Verb):
    """With this verb users can delete an exit of their current room. Since (for now) exits are allways two-way, it also
    deletes the exit from the other room"""

    command = _('deleteexit ')
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
                warning = _(
                    ' 🚧 Keep in mind that the exit "{exit_name}" in "{destination_name}" that leads here has not been deleted.'
                ).format(exit_name=exit_from_there.name, destination_name=destination.name)
            self.session.send_to_client(_(
                'Exit "{exit_name}" has been deleted.\n'
                'It\'s destination was "{destination_name}" (number {destination_alias})\n'
                '{warning}'
            ).format(exit_name=exit_name, destination_name=destination.name, destination_alias=destination.alias, warning=warning))
            exit.delete()
        else:
            self.session.send_to_client(_(
                'There is no room called "{exit_name}".\nTo delete anything you have to enter its exact name.'
            ).format(exit_name=exit_name))

        self.finish_interaction()

    def delete_exit(self, exit_here_name):
        this_room = self.session.user.room
        other_room = self.session.user.room.get_exit(exit_here_name).destination
        
        exit = self.session.user.room.get_exit(exit_here_name).delete()
        # this_room.delete_exit(exit_here_name)
            

class DeleteItem(verb.Verb):
    """By using this verb users can delete items that are in their current room"""

    command = _('deleteitem ')
    permissions = verb.PRIVILEGED

    def process(self, message):
        command_length = len(self.command)
        item_name = message[command_length:]
        selected_item = next(entities.Item.objects(room=self.session.user.room, name=item_name), None)

        if selected_item is None:
            self.session.send_to_client(_(
                "There is not any item called {item_name}.\n"
                "To delete anything you have to enter its exact name."
            ).format(item_name=item_name))
        else:
            selected_item.delete()
            self.session.send_to_client(f'Item "{item_name}" has been deleted.')
        self.finish_interaction()

