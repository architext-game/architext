import functools
import json
import textwrap

import mongoengine

from architext.adapters.sender import MessageOptions

from .. import util
from .. import entities
from . import look, verb

import architext.strings as strings

class LobbyMenu(verb.Verb):
    '''Helper class that has the method that shows the lobby menu'''
    def show_lobby_menu(self):
        out_message = ""

        self.session.world_list_cache = self.get_worlds_list()

        world_list = self.session.world_list_cache
        
        if world_list:
            out_message += _('Enter the number of the world you want to enter\n')
            # Padding is great for desktop but bad for mobile
            # world_names_with_index = [f' {index: < 4} {world.name: <36}  {world.get_connected_users()}{chr(128100)} by {world.creator.name} {"" if world.public else chr(128274)}' for index, world in enumerate(world_list)]
            world_names_with_index = [f' {index+1} {world.name}  [{world.get_connected_users()}{chr(128100)} {world.creator.name}{"" if world.public else f" {chr(128274)}"}]' for index, world in enumerate(world_list)]
            out_message += functools.reduce(lambda a, b: '{}\n{}'.format(a, b), world_names_with_index)
        else:
            out_message += _('There are not public or known private worlds in this server.')
        out_message += '\n\n' + _(
            'Options:\n'
            '  +  to create a new world.\n'
            '  ?  to see all available actions.'
        )
        self.session.send_to_client(out_message)

    def get_worlds_list(self):
        return list(filter(self.has_to_be_listed, entities.World.objects()))

    def has_to_be_listed(self, world):
        if world.public:
            return True
        elif world.creator == self.session.user:
            return True
        elif world in self.session.user.joined_worlds:
            return True
        else:
            return False


class LobbyHelp(LobbyMenu):
    command = '?'
    verbtype = verb.LOBBYVERB

    def process(self, message):
        out_message = _(
            'You can use these commands from the lobby:\n'
            '  +    to create a new world.\n'
            '  -    to delete one of your worlds.\n'
            '  r    to reload and show the list of worlds.\n'
            '  *    to deploy a public world snapshot.\n'
            '  >    to import a world from text.\n'
            '  who  to see who is connected right now.\n'
            '\n'
            'Enter the number of a world in the world list to go there.\n'
            'Enter the invite code of a world to go there.'
        )
        self.session.send_to_client(out_message)
        self.finish_interaction()

    

class GoToLobby(LobbyMenu):
    command = _('exitworld')
    permissions = verb.NOBOT

    def process(self, message):
        self.session.user.leave_world()
        self.show_lobby_menu()
        self.finish_interaction()

class JoinByInviteCode(LobbyMenu):
    command = ''
    verbtype = verb.LOBBYVERB

    @classmethod
    def has_world_id_format(cls, string):
        return len(string.strip()) == 24

    @classmethod
    def can_process(cls, message, session):
        if super().can_process(message, session) and cls.has_world_id_format(message):
            return True
        else:
            return False

    def process(self, message):
        try:
            chosen_world = entities.World.objects.get(id=message)
        except entities.World.DoesNotExist:
            self.session.send_to_client(_("I don't understand that"))
            self.finish_interaction()
            return

        self.session.user.enter_world(chosen_world)
        
        self.session.send_to_client(_("Traveling to {world_name}.").format(world_name=chosen_world.name))
        look.Look(self.session).show_current_room(show_world_name=True)
        self.session.send_to_others_in_room(_("Pof! {player_name} appears here.").format(player_name=self.session.user.name))
        self.finish_interaction()

class EnterWorld(LobbyMenu):
    command = ''
    verbtype = verb.LOBBYVERB

    @classmethod
    def can_process(self, message, session):
        if super().can_process(message, session) and message.isnumeric():
            return True
        else:
            return False

    def __init__(self, session):
        super().__init__(session)
        self.current_process_function = self.process_world_number

    def process(self, message):
        self.current_process_function(message)

    def process_world_number(self, message):
        try:
            index = int(message) - 1
        except ValueError:
            self.session.send_to_client(strings.not_a_number)
            self.finish_interaction()
            return
        
        try:
            if index < 0:
                raise IndexError
            chosen_world = self.session.world_list_cache[index]
        except IndexError:
            self.session.send_to_client(strings.wrong_value)
            self.finish_interaction()
            return

        try:
            location_save = self.session.user.get_location_save(chosen_world)
            self.session.user.enter_world(chosen_world)
        except mongoengine.errors.DoesNotExist:
            self.session.send_to_client(_("This world no longer exists. Enter 'r' to reload the lobby."))
            self.finish_interaction()
            return
        
        self.session.send_to_client(_('{body}')
            .format(
                body=_('Returning to your last location there.') if location_save is not None else _('Going there for the first time!')
        ))

        look.Look(self.session).show_current_room(show_world_name=True)
        self.session.send_to_others_in_room(_("Puufh! {player_name} appears here.").format(player_name=self.session.user.name))
        self.finish_interaction()
        

class RefreshLobby(LobbyMenu):
    verbtype = verb.LOBBYVERB
    command = 'r'

    def process(self, message):
        self.show_lobby_menu()
        self.finish_interaction()

class CreateWorld(LobbyMenu):
    verbtype = verb.LOBBYVERB
    command = '+'

    def process(self, message):
        starting_room = entities.Room(
            name=_('The First of Many Rooms'),
            alias='0',
            description=_(
                'This is the first room of your world. Here you are the Architext!\n'
                '\n'
                'If you don\'t know where to start, just type "help building". There you\'ll find all you need to know to build any kind of world.\n'
                '\n'
                'Remember that you can type "worldinfo" to see the world\'s invite code.'
            )
        )
        self.new_world = entities.World(save_on_creation=False, creator=self.session.user, starting_room=starting_room)
        self.session.send_to_client(_('Enter the name for your new world. ("/" to cancel)'))
        self.process = self.process_word_name

    def process_word_name(self, message):
        if message == "/":
            self.session.send_to_client(strings.cancelled)
            self.finish_interaction()
            return
        if not message:
            self.session.send_to_client(strings.is_empty)
            return


        self.new_world.name = message
        self.new_world.save()
        self.session.send_to_client(_('Your new world is ready'), MessageOptions(display='box'))
        self.session.send_to_client(_(
            'It is a private world 🔒. You can invite your friends sharing this invite code:\n'
            '\n'
            '{invite_code}\n'
            '\n'
            'When it is ready, you can make the world public using the editworld command.\n'
            '\n'
            'Press enter to see your new world...'
        ).format(invite_code=self.new_world.id), MessageOptions(section=False))
        self.process = self.enter_to_continue

    def enter_to_continue(self, message):
        self.session.user.enter_world(self.new_world)
        look.Look(self.session).show_current_room(show_world_name=True)
        self.finish_interaction()


class DeployPublicSnapshot(LobbyMenu):
    verbtype = verb.LOBBYVERB
    command = '*'

    def process(self, message):
        self.public_snapshots = entities.WorldSnapshot.objects(public=True)

        if not self.public_snapshots:
            self.session.send_to_client(_('There are no public worlds to deploy.'))
            self.finish_interaction()
            return

        message = _('Which world do you want to deploy? ("/" to cancel)\n')
        for index, snapshot in enumerate(self.public_snapshots):
            message += '{}. {}\n'.format(index+1, snapshot.name)
        self.session.send_to_client(message)
        self.process = self.process_menu_option

    def process_menu_option(self, message):
        if message == '/':
            self.session.send_to_client(strings.cancelled)
            self.show_lobby_menu()
            self.finish_interaction()
            return
            
        try:
            index = int(message)
            if index < 1:
                raise ValueError
        except ValueError:
            self.session.send_to_client(strings.wrong_value)
            return

        try:
            self.chosen_snapshot = self.public_snapshots[index-1]
        except IndexError:
            self.session.send_to_client(strings.wrong_value)
            return
        
        self.session.send_to_client(_('How do you want to name the new world? ("/" to cancel)'))
        self.process = self.process_new_world_name

    def process_new_world_name(self, message):
        if message == "/":
            self.session.send_to_client(strings.cancelled)
            self.finish_interaction()
            return
        if not message:
            self.session.send_to_client(strings.is_empty)
            return
            
        world_name = message
        self.deploy_at_new_world(self.chosen_snapshot, world_name)
        self.session.send_to_client(_('Done.'))
        self.show_lobby_menu()
        self.finish_interaction()

    def deploy_at_new_world(self, snapshot, world_name):
        snapshot_instance = snapshot.snapshoted_state.clone()
        new_world = entities.World(creator=self.session.user, world_state=snapshot_instance, name=world_name)


class DeleteWorld(LobbyMenu):
    verbtype = verb.LOBBYVERB
    command = '-'

    def process(self, message):
        self.your_worlds = entities.World.objects(creator=self.session.user)

        if not self.your_worlds:
            self.session.send_to_client(_("You have not created any world."))
            self.finish_interaction()
            return

        message = _('Choose the world to delete. YOU WON\'T BE ABLE TO GET IT BACK. Consider making a backup first. ("/" to cancel)\n')
        for index, world in enumerate(self.your_worlds):
            message += "{}. {}\n".format(index+1, world.name)
        self.session.send_to_client(message)
        self.process = self.process_menu_option

    def process_menu_option(self, message):
        if message == '/':
            self.session.send_to_client(strings.cancelled)
            self.show_lobby_menu()
            self.finish_interaction()
            return

        try:
            index = int(message)
            if index < 1:
                raise ValueError
        except ValueError:
            self.session.send_to_client(strings.not_a_number)
            return

        try:
            world_to_delete = self.your_worlds[index-1]
        except IndexError:
            self.session.send_to_client(strings.wrong_value)
            return

        try:
            world_to_delete.delete()
        except entities.CantDelete as e:
            self.session.send_to_client(_("It can not be deleted: {error}".format(error=e)))
        else:
            self.session.send_to_client(_("Done."))

        self.show_lobby_menu()
        self.finish_interaction()


class ImportWorld(LobbyMenu):
    verbtype = verb.LOBBYVERB
    command = '>'

    def process(self, message):
        self.json_message = ''
        self.world_name = ''
        self.session.send_to_client(_('Enter a name for your new world. ("/" to cancel)'))
        self.process = self.process_word_name

    def process_word_name(self, message):
        if message == "/":
            self.session.send_to_client(strings.cancelled)
            self.finish_interaction()
            return
        if not message:
            self.session.send_to_client(strings.is_empty)
            return

        self.world_name = message
        self.session.send_to_client(_(
            'Now paste the text export of the world.\n'
            'It will be automatically divided into multiple messages if it is too long.'
            'The server won\'t consider the text as received until it is valid.\n'
            'If you entered the wrong text, send "/" to cancel.'
        ))
        self.process = self.process_world_json

    def process_world_json(self, message):
        # todo: check for possible risks and outcomes of bad input.
        if message == '/':
            self.session.send_to_client(strings.cancelled)
            self.show_lobby_menu()
            self.finish_interaction()
            return
        self.session.send_to_client(_("{char_number} chars received").format(char_number=len(message)))
        message_valid = False
        message_without_control_characters = util.remove_control_characters(message)
        self.json_message += message_without_control_characters

        self.session.send_to_client(_('Parsing your message. Please wait...'))
        
        world_dict = util.text_to_world_dict(self.json_message)

        if world_dict is not None:
            new_world = util.world_from_dict(world_dict, self.world_name, self.session.user)
            self.session.send_to_client(_('Your new world is ready. The items in all player inventories from the original world have been moved to your inventory.'))
            self.show_lobby_menu()
            self.finish_interaction()
        else:
            self.session.send_to_client(_('The text is still invalid. Waiting for more characters. ("/" to cancel)'))


