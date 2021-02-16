from . import verb
from .. import entities
import functools

_backup_snapshot_name = 'last_world_backup'

class CreateSnapshot(verb.Verb):
    command = 'snapshot'
    permissions = verb.PRIVILEGED

    def __init__(self, session):
        super().__init__(session)        
        self.current_process_function = self.process_first_message
        self.snapshot = entities.WorldSnapshot(save_on_creation=False)

    def process(self, message):
        self.current_process_function(message)

    def process_first_message(self, message):
        self.session.send_to_client("¿Qué nombre quieres ponerle al snapshot?")
        self.current_process_function = self.process_snapshot_name

    def process_snapshot_name(self, message):
        if not message:
            self.session.send_to_client("El nombre no puede estar vacío. Prueba con otro.")
            return

        if message == _backup_snapshot_name:
            self.session.send_to_client("Ese nombre está reservado. prueba con otro.")
            return

        world = self.session.user.room.world_state.get_world()

        self.snapshot.name = message
        self.snapshot.snapshoted_state = self.snapshot_world_state()
        self.snapshot.save()
        world.add_snapshot(self.snapshot)
        self.session.send_to_client('Hecho!')
        self.finish_interaction()
    
    def snapshot_world_state(self):
        new_world_state = self.session.user.room.world_state.clone()
        return new_world_state


class DeploySnapshot(verb.Verb):
    command = 'deploy'
    permissions = verb.PRIVILEGED

    def __init__(self, session):
        super().__init__(session)
        self.current_process_function = self.process_first_message

    def process(self, message):
        self.current_process_function(message)

    def process_first_message(self, message):
        self.show_snapshot_list()
        self.current_process_function = self.process_menu_option

    def process_menu_option(self, message):
        if message == 'x':
            self.session.send_to_client('Cancelado.')
            self.finish_interaction()
            return
        
        try:
            index = int(message)
        except ValueError:
            self.session.send_to_client("Introduce un número")
            return

        world = self.session.user.room.world_state.get_world()
        try:
            chosen_snapshot = world.snapshots[index]
        except IndexError:
            self.session.send_to_client("Introduce el número correspondiente a uno de los snapshots")
            return

        self.deploy_snapshot(chosen_snapshot, world)
        self.session.send_to_client('Hecho! Puedes recuperar el mundo tal y como era antes del despliegue. Para hacerlo, despliega el snapshot "{}".'.format(_backup_snapshot_name))
        self.finish_interaction()

    def show_snapshot_list(self):
        world = self.session.user.room.world_state.get_world()
        snapshots = world.snapshots
        message = '¿Qué snapshot quieres desplegar?\n'
        for i, snapshot in enumerate(snapshots):
            message += '{}. {}\n'.format(i, snapshot.name)
        message += '\n(x para cancelar)'
        self.session.send_to_client(message)

    def deploy_snapshot(self, chosen_snapshot, world):
        new_world_state = chosen_snapshot.snapshoted_state.clone()

        # user evacuation!!
        for old_room in world.world_state.get_rooms():
            for user in old_room.users:
                self.session.send_to_user(user, 'Se ha desplegado un snapshot del mundo en el que estás.')
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
