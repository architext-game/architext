from architext.chatbot.ports.messaging_channel import MessageOptions
from architext.core.commands import Command, EditExit as EditExitCommand, EditItem as EditItemCommand
from architext.core.facade import Architext
from architext.core.queries.get_room_details import ExitInRoomDetails, GetRoomDetails, ItemInRoomDetails
from architext.core.queries.is_name_valid import IsNameValid
from architext.core.settings import EXIT_DESCRIPTION_MAX_LENGTH, EXIT_NAME_MAX_LENGTH, ITEM_DESCRIPTION_MAX_LENGTH, ITEM_NAME_MAX_LENGTH
from . import verb
from .. import util
import textwrap
import architext.chatbot.strings as strings
import logging
from gettext import gettext as _
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from architext.chatbot.session import Session
else:
    Session = object()

class Edit(verb.Verb):
    """This verb allows users to edit properties of an item or exit that is in their current room"""

    command = _('edit ')
    privileges_requirement = 'owner'

    def __init__(self, session: Session, architext: Architext):
        super().__init__(session, architext)
        self.current_process_function = self.start_editing

    def process(self, message):
        if message == '/':
            self.session.sender.send(self.session.user_id, strings.cancelled)
            self.finish_interaction()
        else:
            self.current_process_function(message)

    def start_editing(self, message: str):
        self.current_room = self.architext.query(GetRoomDetails(), self.session.user_id).room

        if self.current_room is None:
            self.session.sender.send(self.session.user_id, strings.room_not_found)
            self.finish_interaction()
            return

        message = message[len(self.command):]

        entities = util.name_to_entity(message, self.current_room)

        if len(entities) > 1: 
            self.session.sender.send(self.session.user_id, strings.many_found)
            self.finish_interaction()
            return
        elif len(entities) == 0:
            self.session.sender.send(self.session.user_id, strings.not_found)
            self.finish_interaction()
            return

        self.entity_to_edit = entities[0]

        if isinstance(self.entity_to_edit, ExitInRoomDetails):
            title = _('Editing exit {exit_name}').format(exit_name=self.entity_to_edit.name)

            body = _(
                'Enter the number of the value to edit.\n'
                '    1 - Name\n'
                '    2 - Description\n'
                '    3 - Visibility\n'
                '    4 - Destination'
            )
            self.session.sender.send_formatted(self.session.user_id, title, body, cancel=True)
            self.current_process_function = self.process_exit_edit_option_number
        else:  # editing an Item
            title = _('Editing item {item_name}').format(item_name=self.entity_to_edit.name)
            body = _(
                'Enter the number of the value to edit.\n'
                '    1 - Name\n'
                '    2 - Description\n'
                '    3 - Visibility'
            )
            self.session.sender.send_formatted(self.session.user_id, title, body, cancel=True)
            self.current_process_function = self.process_item_edit_option_number


    def process_item_edit_option_number(self, message: str):
        try:
            selected_number = int(message)
        except ValueError:
            self.session.sender.send(self.session.user_id, strings.not_a_number)
            return
        
        object_to_edit = self.entity_to_edit

        if selected_number == 1:
            self.option_number = selected_number
            self.session.sender.send(self.session.user_id, _('Enter the new name:'), options=MessageOptions(fillInput=object_to_edit.name))
            self.current_process_function = self.process_reform_value
        elif selected_number == 2:
            self.option_number = selected_number
            self.session.sender.send(self.session.user_id, _('Enter the new description:'), options=MessageOptions(fillInput=object_to_edit.description))
            self.current_process_function = self.process_reform_value
        elif selected_number == 3:
            self.option_number = selected_number
            self.session.sender.send(self.session.user_id, 
                _('Choose the new visibility:\n') +
                strings.visibility_list
            )
            self.current_process_function = self.process_reform_value
        else:
            self.session.sender.send(self.session.user_id, _('Please enter the value of one of the options.'))

    def process_exit_edit_option_number(self, message: str):
        try:
            selected_number = int(message)
        except ValueError:
            self.session.sender.send(self.session.user_id, strings.not_a_number)
            return

        if selected_number == 4:
            self.option_number = selected_number
            self.session.sender.send(self.session.user_id, _('Enter the room number of the new destination. You can find it using the "info" command.'))
            self.current_process_function = self.process_reform_value
        else:
            self.process_item_edit_option_number(message)
    
    def process_reform_value(self, message: str):
        assert self.current_room is not None
        
        if len(message) == 0:
            self.session.sender.send(self.session.user_id, strings.is_empty)
            return
        
        editing_exit = isinstance(self.entity_to_edit, ExitInRoomDetails)
        command: Command

        if self.option_number == 1:  # edit name
            if len(message) == 0:
                self.session.sender.send(self.session.user_id, strings.is_empty)
                return
            if self.architext.query(IsNameValid(name=message, in_room_id=self.current_room.id), self.session.user_id).error == 'duplicated':
                self.session.sender.send(self.session.user_id, strings.room_name_clash)
                return
            if editing_exit:
                if len(message) > EXIT_NAME_MAX_LENGTH:
                    self.session.sender.send(self.session.user_id, strings.too_long.format(limit=EXIT_NAME_MAX_LENGTH))
                    return
                command = EditExitCommand(
                    room_id=self.current_room.id,
                    exit_name=self.entity_to_edit.name,
                    new_name=message
                )
            else:
                if len(message) > ITEM_NAME_MAX_LENGTH:
                    self.session.sender.send(self.session.user_id, strings.too_long.format(limit=ITEM_NAME_MAX_LENGTH))
                    return
                command = EditItemCommand(
                    room_id=self.current_room.id,
                    item_name=self.entity_to_edit.name,
                    new_name=message
                )
        elif self.option_number == 2:  # edit description
            if editing_exit:
                if len(message) > EXIT_DESCRIPTION_MAX_LENGTH:
                    self.session.sender.send(self.session.user_id, strings.too_long.format(limit=EXIT_DESCRIPTION_MAX_LENGTH))
                    return
                command = EditExitCommand(
                    room_id=self.current_room.id,
                    exit_name=self.entity_to_edit.name,
                    new_description=message
                )
            else:
                if len(message) > ITEM_DESCRIPTION_MAX_LENGTH:
                    self.session.sender.send(self.session.user_id, strings.too_long.format(limit=ITEM_DESCRIPTION_MAX_LENGTH))
                    return
                command = EditItemCommand(
                    room_id=self.current_room.id,
                    item_name=self.entity_to_edit.name,
                    new_description=message
                )
        elif self.option_number == 3:  # edit visibility
            if message.lower() in strings.unlisted_input_options:
                new_visibility = "unlisted"
            if message.lower() in strings.auto_input_options:
                new_visibility = "auto"
            elif message.lower() in strings.listed_input_options:
                new_visibility = "listed"
            elif message.lower() in strings.hidden_input_options:
                new_visibility = "hidden"
            else:
                self.session.sender.send(self.session.user_id, strings.wrong_value)
                return

            command = EditExitCommand(
                room_id=self.current_room.id,
                exit_name=self.entity_to_edit.name,
                new_visibility=new_visibility
            ) if editing_exit else EditItemCommand(
                room_id=self.current_room.id,
                item_name=self.entity_to_edit.name,
                new_visibility=new_visibility
            )
        else:  # self.option_number == 4: edit exit's destination
            destination_room = self.architext.query(GetRoomDetails(room_id=message), self.session.user_id)
            if destination_room.room:
                command = EditExitCommand(
                    room_id=self.current_room.id,
                    exit_name=self.entity_to_edit.name,
                    new_destination=destination_room.room.id,
                )
            else:
                self.session.sender.send(self.session.user_id, strings.room_not_found)
                return
        
        if isinstance(command, EditExitCommand):
            self.architext.handle(command, self.session.user_id)
        else:
            self.architext.handle(command, self.session.user_id)
        # This is an error according to mypy:
        # self.architext.handle(command, self.session.user_id)

        self.session.sender.send(self.session.user_id, _('Edition completed.'))
        self.finish_interaction()
