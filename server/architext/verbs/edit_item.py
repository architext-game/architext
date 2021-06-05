from . import verb
from .. import util
from .. import entities
import textwrap
import architext.strings as strings

class EditItem(verb.Verb):
    """This verb allows users to edit properties of an item or exit that is in their current room"""

    command = _('edit ')
    permissions = verb.PRIVILEGED

    def __init__(self, session):
        super().__init__(session)
        self.option_number = None
        self.item_to_edit = None
        self.exit_to_edit = None
        self.current_process_function = self.start_editing

    def process(self, message):
        if message == '/':
            self.session.send_to_client(strings.cancelled)
            self.finish_interaction()
        else:
            self.current_process_function(message)

    def start_editing(self, message):
        current_room = self.session.user.room
        message = message[len(self.command):]
        saved_items = entities.Item.objects(saved_in=self.session.user.room.world_state)

        selected_entity = util.name_to_entity(self.session, message, loose_match=["saved_items"], substr_match=["room_items", "inventory", "room_exits"])

        if selected_entity == "many":
            self.session.send_to_client(strings.many_found)
            self.finish_interaction()
            return
        elif selected_entity is None:
            self.session.send_to_client(strings.not_found)
            self.finish_interaction()
            return

        if isinstance(selected_entity, entities.Item):
            self.item_to_edit = selected_entity

            if self.item_to_edit.is_saved():
                title = _('Editing saved item {item_id}').format(item_id=self.item_to_edit.item_id)
            else:
                title = _('Editing item {item_name}').format(item_name=self.item_to_edit.name)

            body = _(
                'Enter the number of the value to edit.\n'
                '    0 - Name\n'
                '    1 - Description\n'
                '    2 - Visibility'
            )
            out_message = strings.format(title, body, cancel=True)
            self.session.send_to_client(out_message)
            self.current_process_function = self.process_item_edit_option_number

        elif isinstance(selected_entity, entities.Exit):
            self.exit_to_edit = selected_entity

            title = _('Editing exit {exit_name}').format(exit_name=self.exit_to_edit.name)
            body = _(
                'Enter the number of the value to edit.\n'
                '    0 - Name\n'
                '    1 - Description\n'
                '    2 - Visibility\n'
                '    3 - Destination'
            )
            out_message = strings.format(title, body, cancel=True)

            self.session.send_to_client(out_message)
            self.current_process_function = self.process_exit_edit_option_number

        else:
            raise ValueError(f"Expected Room or Exit, {type(selected_entity)} found")


    def process_item_edit_option_number(self, message):
        try:
            message = int(message)
        except ValueError:
            self.session.send_to_client(strings.not_a_number)
            return

        # max_number = 2
        if 0 <= message <= 1:
            self.option_number = message
            self.session.send_to_client(_('Enter the new value:'))
            self.current_process_function = self.process_reform_value
        elif message == 2:
            self.option_number = message
            self.session.send_to_client(
                _('Choose the new visibility:\n') +
                strings.visibility_list
            )
            self.current_process_function = self.process_reform_value
        else:
            self.session.send_to_client(_('Please enter the value of one of the options.'))

    def process_exit_edit_option_number(self, message):
        try:
            message = int(message)
        except ValueError:
            self.session.send_to_client(strings.not_a_number)
            return

        if message == 3:
            self.option_number = message
            self.session.send_to_client(_('Enter the room number of the new destination. You can find it using the "info" command.'))
            self.current_process_function = self.process_reform_value
        else:
            self.process_item_edit_option_number(message)
    
    def process_reform_value(self, message):
        object_to_edit = self.item_to_edit if self.item_to_edit else self.exit_to_edit
        
        if message:
            if self.option_number == 0:  # edit name
                object_to_edit.name = message
                try:
                    object_to_edit.ensure_i_am_valid()
                except entities.NameNotGloballyUnique:
                    self.session.send_to_client(_('There is another entity with that name in this world. Since the item you are editing is takable, it needs an unique name. Enter another name.'))
                    return
                except entities.EmptyName:
                    self.session.send_to_client(strings.is_empty)
                    return
                except entities.WrongNameFormat:
                    self.session.send_to_client(strings.wrong_format)
                    return
                except entities.RoomNameClash:
                    self.session.send_to_client(strings.room_name_clash)
                    return
                except entities.TakableItemNameClash:
                    self.session.send_to_client(strings.takable_name_clash)
                    return
            elif self.option_number == 1:  # edit description
                object_to_edit.description = message
            elif self.option_number == 2:  # edit visibility
                if message.lower() in strings.visible_input_options:
                    object_to_edit.visible = 'obvious'
                elif message.lower() in strings.listed_input_options:
                    object_to_edit.visible = 'listed'
                elif message.lower() in strings.hidden_input_options:
                    object_to_edit.visible = 'hidden'
                elif message.lower() in strings.takable_input_options:
                    if self.can_change_to_takable(self.item_to_edit):
                        object_to_edit.visible = 'takable'
                    else:
                        self.session.send_to_client(_('There is another entity with that name in this world. Since you are trying to make this item takable, it needs an unique name.\nEdition cancelled.'))
                        self.finish_interaction()
                        return
                else:
                    self.session.send_to_client(strings.wrong_value)
                    return
            elif self.option_number == 3:  # edit exit's destination
                if entities.Room.objects(alias=message):
                    object_to_edit.destination = entities.Room.objects(alias=message).first()
                else:
                    self.session.send_to_client(strings.room_not_found)
                    self.finish_interaction()
                    return
            object_to_edit.save()
            self.session.send_to_client(_('Edition completed.'))
            self.finish_interaction()
        else:
            self.session.send_to_client(strings.is_empty)


    def can_change_to_takable(self, item_to_change):
        return entities.Item.name_is_valid(item_to_change.name, item_to_change.room, ignore_item=item_to_change, takable=True)
