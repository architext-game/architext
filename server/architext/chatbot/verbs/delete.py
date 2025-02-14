from architext.core.queries.get_room_details import ExitInRoomDetails, GetRoomDetails
from architext.core.commands import DeleteItem as DeleteItemCommand, DeleteExit as DeleteExitCommand
from architext.core.queries.get_thing_in_room import GetThingInRoom, ItemInRoom, ExitInRoom
from . import verb
from gettext import gettext as _
from architext.chatbot import strings
from architext.chatbot import util

class Delete(verb.Verb):
    command = _('delete ')
    privileges_requirement = 'owner'

    def process(self, message: str):
        self.current_room = self.architext.query(GetRoomDetails(), self.session.user_id).room

        if self.current_room is None:
            self.session.sender.send(self.session.user_id, strings.room_not_found)
            self.finish_interaction()
            return

        message = message[len(self.command):]

        result = self.architext.query(GetThingInRoom(partial_name=message), self.session.user_id)

        if result.status == 'multiple_matches': 
            self.session.sender.send(self.session.user_id, strings.many_found)
            self.finish_interaction()
            return
        elif result.status == 'none_found':
            self.session.sender.send(self.session.user_id, _(
                'There is not any exit or item called "{name}" here.'
            ).format(name=message))
            self.finish_interaction()
            return
        elif result.status == 'exit_matched':
            exit = result.exit_match
            assert exit is not None
            exit_details = util.get_by_name(exit.name, self.current_room.exits)
            destination_room = self.architext.query(GetRoomDetails(room_id=exit_details.destination_id), self.session.user_id).room
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
            self.architext.handle(DeleteExitCommand(
                room_id=self.current_room.id,
                exit_name=exit.name
            ), self.session.user_id)
        elif result.status == 'item_matched':
            assert result.item_match is not None
            self.architext.handle(DeleteItemCommand(
                room_id=self.current_room.id,
                item_name=result.item_match.name
            ), self.session.user_id)
            self.session.sender.send(self.session.user_id, _('Item "{item_name}" has been deleted.').format(item_name=result.item_match.name))

        self.finish_interaction()




