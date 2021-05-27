from . import verb
from .. import entities
import functools
import sandboxmud.strings as strings

_backup_snapshot_name = 'last_world_backup'

class CreateSnapshot(verb.Verb):
    command = _('snapshot')
    permissions = verb.PRIVILEGED

    def __init__(self, session):
        super().__init__(session)        
        self.current_process_function = self.process_first_message
        self.snapshot = entities.WorldSnapshot(save_on_creation=False)

    def process(self, message):
        if message == '/':
            self.session.send_to_client(strings.cancelled)
            self.finish_interaction()
        else:
            self.current_process_function(message)

    def process_first_message(self, message):
        title = _('You are creating a snapshot')
        body  = _(
            'The snapshot will save this world as it is now, and you would be able to return to this state anytime you want.\n'
            '\n'
            'Enter a name for your snapshot:'
        )
        out_message = strings.format(title, body, cancel=True)
        self.session.send_to_client(out_message)
        self.current_process_function = self.process_snapshot_name

    def process_snapshot_name(self, message):
        if not message:
            self.session.send_to_client(strings.is_empty)
            return

        if message == _backup_snapshot_name:
            self.session.send_to_client(_("That name is reserved. Try anothe one."))
            return

        world = self.session.user.room.world_state.get_world()

        self.snapshot.name = message
        self.snapshot.snapshoted_state = self.snapshot_world_state()
        self.snapshot.save()
        world.add_snapshot(self.snapshot)
        self.session.send_to_client(_('Snapshot created. You can use "deploy" to see and restore your snapshots.'))
        self.finish_interaction()
    
    def snapshot_world_state(self):
        new_world_state = self.session.user.room.world_state.clone()
        return new_world_state


class DeploySnapshot(verb.Verb):
    command = _('deploy')
    permissions = verb.PRIVILEGED

    def __init__(self, session):
        super().__init__(session)
        self.current_process_function = self.process_first_message

    def process(self, message):
        if message == '/':
            self.session.send_to_client(strings.cancelled)
            self.finish_interaction()
        else:
            self.current_process_function(message)

    def process_first_message(self, message):
        self.show_world_snapshot_list()
        self.current_process_function = self.process_menu_option

    def process_menu_option(self, message):
        if message == '/':
            self.session.send_to_client(strings.cancelled)
            self.finish_interaction()
            return
            
        try:
            index = int(message)
            if index < 0:
                raise ValueError
        except ValueError:
            self.session.send_to_client(strings.not_a_number)
            return

        world = self.session.user.room.world_state.get_world()

        snapshots = world.snapshots

        try:
            chosen_snapshot = snapshots[index]
        except IndexError:
            self.session.send_to_client(strings.wrong_value)
            return

        if chosen_snapshot is not None:
            world = self.session.user.room.world_state.get_world()
            self.deploy_snapshot(chosen_snapshot, world)
            self.session.send_to_client(_('"{snapshot_name}" has been deployed. The state before the deploy has been snapshoted as {world_backup_name}. Please note that if you deploy a new snapshot, the backup will be overwritten.').format(snapshot_name=chosen_snapshot.name, world_backup_name=_backup_snapshot_name))
            self.finish_interaction()

    def show_world_snapshot_list(self):
        world = self.session.user.room.world_state.get_world()
        
        if not world.snapshots:
            self.session.send_to_client(_('This world has no snaphots to deploy.'))
            self.finish_interaction()
            return

        message = 'Enter the number of the snapshot to deploy\n'

        snapshots = world.snapshots

        for i, snapshot in enumerate(snapshots):
            message += ' {} - {}\n'.format(i, snapshot.name)

        self.session.send_to_client(message)

    def deploy_snapshot(self, chosen_snapshot, world):
        new_world_state = chosen_snapshot.snapshoted_state.clone()

        # user evacuation!!
        for old_room in world.world_state.get_rooms():
            for user in old_room.users:
                if user != self.session.user:
                    self.session.send_to_user(user, _('A snapshot has been deployed on this world.'))
                corresponding_new_room = next(entities.Room.objects(world_state=new_world_state, alias=old_room.alias), None)
                if corresponding_new_room is not None:
                    user.teleport(corresponding_new_room)
                else:
                    user.teleport(new_world_state.starting_room)

        self.save_as_backup(world.world_state, world)
        world.world_state = new_world_state
        world.save()

    def save_as_backup(self, world_state, world):
        backup_snapshot = next(filter(lambda s: s.name==_backup_snapshot_name, world.snapshots), None)

        if backup_snapshot is None:
            backup_snapshot = entities.WorldSnapshot(name=_backup_snapshot_name, snapshoted_state=world_state)
            world.add_snapshot(backup_snapshot)
        else:
            old_backup = backup_snapshot.snapshoted_state
            backup_snapshot.snapshoted_state = world_state
            backup_snapshot.save()
            old_backup.delete()


class PubishSnapshot(verb.Verb):
    command = _('publish')
    permissions = verb.CREATOR

    def process(self, message):
        self.show_world_snapshot_list()
        self.process = self.process_menu_option

    def process_menu_option(self, message):
        if message == '/':
            self.session.send_to_client(strings.cancelled)
            self.finish_interaction()
            return
            
        try:
            index = int(message)
            if index < 0:
                raise ValueError
        except ValueError:
            self.session.send_to_client(strings.not_a_number)
            return

        world = self.session.user.room.world_state.get_world()

        publishable_snapshots = list(filter(lambda s: s.public==False and s.name!=_backup_snapshot_name, world.snapshots))

        try:
            chosen_snapshot = publishable_snapshots[index]
        except IndexError:
            self.session.send_to_client(strings.wrong_value)
            return

        if chosen_snapshot is not None:
            chosen_snapshot.publish()
            self.session.send_to_client(_('The snapshot has been published!'))
            self.finish_interaction()

    def show_world_snapshot_list(self):
        world = self.session.user.room.world_state.get_world()
        publishable_snapshots = list(filter(lambda s: s.public==False and s.name!=_backup_snapshot_name, world.snapshots))

        if not publishable_snapshots:
            self.session.send_to_client(_('This world has no snapshots to publish'))
            self.finish_interaction()
            return
        
        title = _('You are publishing a snapshot')
        body = _(
            'After it is published, any player will be able to create a new world based on the snapshost.\n'
            'Publishing snapshots is useful for worlds containing puzzles that can only be solved once.\n'
            '\n'
            'Enter the number of the snapshot to publish\n'
        )

        for i, snapshot in enumerate(publishable_snapshots):
            body += ' {} - {}\n'.format(i, snapshot.name)

        out_message = strings.format(title, body, cancel=True)
        self.session.send_to_client(out_message)


class UnpubishSnapshot(verb.Verb):
    command = _('unpublish')
    permissions = verb.CREATOR

    def process(self, message):
        self.show_published_snapshot_list()
        self.process = self.process_menu_option

    def process_menu_option(self, message):
        if message == '/':
            self.session.send_to_client(strings.cancelled)
            self.finish_interaction()
            return
            
        try:
            index = int(message)
            if index < 0:
                raise ValueError
        except ValueError:
            self.session.send_to_client(strings.not_a_number)
            return

        your_worlds = entities.World.objects(creator=self.session.user)
        your_public_snapshots = [(snapshot, world) for world in your_worlds for snapshot in world.snapshots if snapshot.public]

        try:
            chosen_snapshot = your_public_snapshots[index][0]
        except IndexError:
            self.session.send_to_client(strings.wrong_value)
            return
        
        if chosen_snapshot is not None:
            chosen_snapshot.unpublish()
            self.session.send_to_client(_('The snapshot has been unpublished'))
            self.finish_interaction()

    def show_published_snapshot_list(self):
        your_worlds = entities.World.objects(creator=self.session.user)
        your_public_snapshots = [(snapshot, world) for world in your_worlds for snapshot in world.snapshots if snapshot.public]

        if len(your_public_snapshots) == 0:
            self.session.send_to_client(_('There are not published snapshots in this world.'))
            self.finish_interaction()
            return

        message = _('Enter the number of the snapshot to unpublish ("/" to cancel)\n')

        for i, (snapshot, world) in enumerate(your_public_snapshots):
            message += _(' {index} - {snapshot_name: <24} World: {world_name}\n').format(index=i, snapshot_name=snapshot.name, world_name=world.name)

        self.session.send_to_client(message)


class DeleteSnapshot(verb.Verb):
    command = _('deletesnapshot')
    permissions = verb.CREATOR

    def process(self, message):
        self.show_world_snapshot_list()
        self.process = self.process_menu_option

    def show_world_snapshot_list(self):
        world = self.session.user.room.world_state.get_world()
        self.deletable_snapshots = list(filter(lambda s: s.public==False, world.snapshots))

        if not self.deletable_snapshots:
            self.session.send_to_client(_('This world has no snapshots to delete. If you want to delete a public one, first unpublish it.'))
            self.finish_interaction()
            return
        
        message = _(
            'If you want to delete a public snapshot, you need to unpublish it first\n'
            '\n'
            'Enter the number of the snapshots to delete ("/" to cancel)\n'
        )

        for i, snapshot in enumerate(self.deletable_snapshots):
            message += ' {} - {}\n'.format(i, snapshot.name)

        self.session.send_to_client(message)

    def process_menu_option(self, message):
        if message == '/':
            self.session.send_to_client(strings.cancelled)
            self.finish_interaction()
            return

        try:
            index = int(message)
            if index < 0:
                raise ValueError
        except ValueError:
            self.session.send_to_client(srings.not_a_number)
            return

        try:
            chosen_snapshot = self.deletable_snapshots[index]
        except IndexError:
            self.session.send_to_client(strings.wrong_value)
            return

        chosen_snapshot.delete()
        self.session.send_to_client(_('Snapshot deleted'))
        self.finish_interaction()
