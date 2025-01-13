from gettext import gettext as _

from architext.core.commands import GetCurrentRoom

from architext.chatbot.ports.sender import AbstractSender, MessageOptions
from architext.core.messagebus import MessageBus
from architext.core.ports.unit_of_work import UnitOfWork
from .verb import Verb
from .. import strings

class Look(Verb):
    """Shows room and items info to players"""

    command = _('look')

    def process(self, message: str):
        # command_length = len(self.command) + 1
        # if message[command_length:]:
        #     self.show_item_or_exit(message[command_length:])
        # else:
        #     self.show_current_room()
        show_current_room(
            messagebus=self.messagebus,
            sender=self.session.sender,
            uow=self.uow,
            user_id=self.session.user_id
        )
        self.finish_interaction()

    # def show_item_or_exit(self, partial_name):
    #     selected_entity = util.name_to_entity(self.session, partial_name, substr_match=['room_items', 'room_exits', 'inventory'])

    #     if selected_entity == 'many':
    #         self.session.send_to_client(strings.many_found)
    #     elif selected_entity is None:
    #         self.session.send_to_client(strings.not_found)
    #     else:
    #         self.session.send_to_client(f"👁 {selected_entity.name}\n{selected_entity.description if selected_entity.description else strings.default_description}")
    

def show_current_room(sender: AbstractSender, messagebus: MessageBus, uow: UnitOfWork, user_id: str, show_world_name: bool = False) -> None:
    result = messagebus.handle(uow, GetCurrentRoom(), user_id)

    if result.current_room is None:
        sender.send(user_id, _("You are not in a room!"))
        return

    room = result.current_room

    title = room.name
    description = (room.description if room.description else strings.default_description) + '\n'

    # listed_exits = [exit.name for exit in room.exits if exit.is_listed()]
    listed_exits = [exit.name for exit in room.exits]
    if len(listed_exits) > 0:
        exits = (', '.join(listed_exits))
        exits = _("⮕ Exits: {exits}.\n").format(exits=exits)
    else:
        exits = ""

    items = ''
    # listed_items = [item.name for item in room.items if item.is_listed()]
    # if len(listed_items) > 0:
    #     items = _('👁 You see ')+(', '.join(listed_items))
    #     items = items + '.\n'
    # else:
    #     items = ''

    # players_here = [user for user in room.people if user != self.session.user]
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