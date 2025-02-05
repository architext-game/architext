from architext.core.queries.get_room_details import ExitInRoomDetails, GetRoomDetails
from architext.core.commands import DeleteItem as DeleteItemCommand, DeleteExit as DeleteExitCommand
from . import verb
from gettext import gettext as _
from architext.chatbot import strings
from architext.chatbot import util

class Delete(verb.Verb):
    """With this verb users can delete an exit of their current room. Since (for now) exits are allways two-way, it also
    deletes the exit from the other room"""

    command = _('delete ')

    def process(self, message: str):
        self.current_room = self.architext.query(GetRoomDetails(), self.session.user_id).room

        if self.current_room is None:
            self.session.sender.send(self.session.user_id, strings.room_not_found)
            self.finish_interaction()
            return

        message = message[len(self.command):]

        entities = util.name_to_entity(message, self.current_room, match='strict')

        if len(entities) > 1: 
            self.session.sender.send(self.session.user_id, strings.many_found)
            self.finish_interaction()
            return
        elif len(entities) == 0:
            self.session.sender.send(self.session.user_id, _(
                'There is not any exit or item called "{name}" here.\n'
                'To delete something you have to enter its exact name.'
            ).format(name=message))
            self.finish_interaction()
            return

        self.entity_to_delete = entities[0]

        # if self.entity_to_delete.is_saved():
        #     title = _('Editing saved item {item_id}').format(item_id=self.entity_to_delete.item_id)
        # else:
        if isinstance(self.entity_to_delete, ExitInRoomDetails):
            exit = self.entity_to_delete
            destination_room = self.architext.query(GetRoomDetails(), self.session.user_id).room
            warning = ''
            if destination_room:
                warning += 'It\'s destination was "{destination_name}" (id {destination_id})\n'.format(
                    destination_name=destination_room.name, destination_id=destination_room.id
                )
                exit_from_there = next((
                    exit for exit in destination_room.exits 
                    if exit.destination_id == destination_room.id
                ), None)
                if exit_from_there is not None:
                    warning += _(
                        '\n 🚧 Keep in mind that the exit "{exit_name}" in "{destination_name}" that leads here has not been deleted.'
                    ).format(exit_name=exit_from_there.name, destination_name=destination_room.name)
            self.session.sender.send(self.session.user_id, _(
                'Exit "{exit_name}" has been deleted.\n'
                '{warning}'
            ).format(exit_name=exit.name, warning=warning))
            a = "asdas"
            self.architext.handle(DeleteExitCommand(
                room_id=self.current_room.id,
                exit_name=exit.name
            ), self.session.user_id)
        else:  # isinstance(self.entity_to_delete, ItemInRoomDetails):
            self.architext.handle(DeleteItemCommand(
                room_id=self.current_room.id,
                item_name=self.entity_to_delete.name
            ), self.session.user_id)
            self.session.sender.send(self.session.user_id, _('Item "{item_name}" has been deleted.').format(item_name=self.entity_to_delete.name))

        self.finish_interaction()

# class DeleteRoom(verb.Verb):
#     """This verb allows users to delete their current room.
#     A room where there are other connected players cannot be deleted.
#     Also, the initial room (with alias 0) cannot be deleted.
#     Note that rooms may be left disconnected after the use of this command"""

#     command = _('deleteroom')
#     permissions = verb.PRIVILEGED

#     def process(self, message):
#         room_to_delete = self.session.user.room

#         if len([user for user in entities.User.objects(room=room_to_delete) if user.client_id != None]) > 1:
#             self.session.send_to_client(_("You can't delete the room if there are other players here."))
#         if room_to_delete.alias == "0":
#             self.session.send_to_client(_('You can\'t delete the starting room. But you can edit it if you don\'t like it :-)'))
#         else:
#             # exits connecting to this room are implicitly removed from db and from exit lists in all rooms, due to its definition in entities.py

#             for item in room_to_delete.items:
#                 item.delete()

#             for exit in room_to_delete.exits:
#                 exit.delete()

#             room_to_escape_from_oblivion = self.session.user.room.world_state.starting_room
#             self.session.user.teleport(room_to_escape_from_oblivion)
#             for user in entities.User.objects(room=room_to_delete):
#                 user.teleport(room_to_escape_from_oblivion)

#             room_to_delete.delete()
#             self.session.send_to_client(_("The room and the exits leading to it have been deleted."))
            
#         self.finish_interaction()


