from . import verb
from .. import entities
import architext.service_layer.services as services
import architext.service_layer.exceptions as exceptions

class DeleteRoom(verb.Verb):
    """This verb allows users to delete their current room.
    A room where there are other connected players cannot be deleted.
    Also, the initial room (with alias 0) cannot be deleted.
    Note that rooms may be left disconnected after the use of this command"""

    command = _('deleteroom')
    permissions = verb.PRIVILEGED

    def process(self, message):
        try:
            services.delete_room(self.session, self.session.user.room.id)
        except exceptions.CantDeleteRoomWithPlayers:
            self.session.send_to_client(_("You can't delete the room if there are other players here."))
        except exceptions.CantDeleteStartingRoom:
            self.session.send_to_client(_('You can\'t delete the starting room. But you can edit it if you don\'t like it :-)'))
        else:
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
                    '\n 🚧 Keep in mind that the exit "{exit_name}" in "{destination_name}" that leads here has not been deleted.'
                ).format(exit_name=exit_from_there.name, destination_name=destination.name)
            self.session.send_to_client(_(
                'Exit "{exit_name}" has been deleted.\n'
                'It\'s destination was "{destination_name}" (number {destination_alias})\n'
                '{warning}'
            ).format(exit_name=exit_name, destination_name=destination.name, destination_alias=destination.alias, warning=warning))
            services.delete_exit(self.session, exit_id=exit.id)
        else:
            self.session.send_to_client(_(
                'There is not any exit called "{exit_name}" here.\nTo delete anything you have to enter its exact name.'
            ).format(exit_name=exit_name))

        self.finish_interaction()


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
            services.delete_item(self.session, selected_item.id)
            self.session.send_to_client(_('Item "{item_name}" has been deleted.').format(item_name=item_name))
        self.finish_interaction()

