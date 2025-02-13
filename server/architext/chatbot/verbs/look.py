from gettext import gettext as _

from architext.chatbot.sender import Sender, MessageOptions
from architext.core import Architext
from architext.core.queries.get_current_room import GetCurrentRoom
from architext.core.queries.get_thing_in_room import GetThingInRoom
from .verb import Verb
from .. import strings

class Look(Verb):
    """Shows room and items info to players"""

    command = _('look')

    def process(self, message: str):
        command_length = len(self.command) + 1
        if message[command_length:]:
            self.show_item_or_exit(message[command_length:])
        else:
            show_current_room(
                sender=self.session.sender,
                user_id=self.session.user_id,
                architext=self.architext
            )
        self.finish_interaction()

    def show_item_or_exit(self, partial_name: str):
        result = self.architext.query(GetThingInRoom(partial_name=partial_name), self.session.user_id)

        if result.status == "multiple_matches":
            self.session.sender.send(self.session.user_id, strings.many_found)
        elif result.status == "none_found":
            self.session.sender.send(self.session.user_id, strings.not_found)
        elif result.status == "exit_matched":
            assert result.exit_match is not None
            self.session.sender.send(self.session.user_id, f"👁 {result.exit_match.name}\n{result.exit_match.description if result.exit_match.description else strings.default_description}")
        elif result.status == "item_matched":
            assert result.item_match is not None
            self.session.sender.send(self.session.user_id, f"👁 {result.item_match.name}\n{result.item_match.description if result.item_match.description else strings.default_description}")
    

def show_current_room(sender: Sender, architext: Architext, user_id: str, show_world_name: bool = False) -> None:
    result = architext.query(GetCurrentRoom(), user_id)

    if result.current_room is None:
        sender.send(user_id, _("You are not in a room!"))
        return

    room = result.current_room

    title = room.name
    description = (room.description if room.description else strings.default_description) + '\n'

    listed_exits = [exit.name for exit in room.exits if exit.list_in_room_description]
    if len(listed_exits) > 0:
        exits = (', '.join(listed_exits))
        exits = _("⮕ Exits: {exits}.\n").format(exits=exits)
    else:
        exits = ""

    items = ''

    listed_items = [item.name for item in room.items if item.list_in_room_description]
    if len(listed_items) > 0:
        items = _('👁 You see ')+(', '.join(listed_items))
        items = items + '.\n'
    else:
        items = ''

    player_names = [user.name for user in room.people]
    if len(player_names) < 1:
        players_description = ""
    elif len(player_names) == 1:
        players_description = _("{player_name} is here").format(player_name=player_names[0])
    else:
        players_list = ', '.join([f'{name}' for name in player_names])
        players_description = _("Players here: {players_list}").format(players_list=players_list)
    players_description = f'👤 {players_description}.' + '\n' if players_description != '' else ''
    line_break = '\n' if (items or players_description or exits) else ''
    message = (f"{description}{line_break}{items}{players_description}{exits}")
    
    if show_world_name:
        pass
        # world_name = _('You are in ') + room.world_state.get_world().name
        # self.session.send_to_client(world_name, MessageOptions(display='box'))
        # self.session.send_to_client(title, MessageOptions(section=False, display='underline'))
        # self.session.send_to_client(message, MessageOptions(section=False))
    else:
        sender.send(user_id, title, options=MessageOptions(display='underline'))
        sender.send(user_id, message, options=MessageOptions(section=False))