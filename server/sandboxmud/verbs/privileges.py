from . import verb
from .. import entities


class MakeEditor(verb.Verb):
    command = _('makeeditor ')
    permissions = verb.CREATOR

    def process(self, message):
        target_user_name = message[len(self.command):]
        target_user = next(entities.User.objects(name=target_user_name), None)
        world = self.session.user.room.world_state.get_world()

        if target_user is not None:
            world.add_editor(target_user)
            self.session.send_to_client(_('{user_name} is now an editor in {world_name}.').format(user_name=target_user.name, world_name=world.name))
            self.session.send_to_user(target_user, _('You just become an editor in {world_name}!').format(world_name=world.name))
        else:
            self.session.send_to_client(_('That user does not exist'))

        self.finish_interaction()


class RemoveEditor(verb.Verb):
    command = _('removeeditor ')
    permissions = verb.CREATOR

    def process(self, message):
        target_user_name = message[len(self.command):]
        target_user = next(entities.User.objects(name=target_user_name), None)
        world = self.session.user.room.world_state.get_world()

        if target_user is not None:
            if target_user in world.editors:
                world.remove_editor(target_user)
                self.session.send_to_client(_('{user_name} is no longer an editor in {world_name}.').format(user_name=target_user.name, world_name=world.name))
                self.session.send_to_user(target_user, _('You are no longer an editor in {world_name}').format(world_name=world.name))
            else:
                self.session.send_to_client(_('That user is not an editor in this world.'))
        else:
            self.session.send_to_client(_('That user does not exist.'))

        self.finish_interaction()
        

