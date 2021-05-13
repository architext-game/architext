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
        if message == '/':
            self.session.send_to_client("Creación de snapshot cancelada.")
            self.finish_interaction()
        else:
            self.current_process_function(message)

    def process_first_message(self, message):
        self.session.send_to_client("¿Qué nombre quieres ponerle al snapshot? ('/' para cancelar)")
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
        self.session.send_to_client('Snapshot creado.')
        self.finish_interaction()
    
    def snapshot_world_state(self):
        new_world_state = self.session.user.room.world_state.clone()
        return new_world_state


class DeploySnapshot(verb.Verb):
    command = 'desplegar'
    permissions = verb.PRIVILEGED

    def __init__(self, session):
        super().__init__(session)
        self.current_process_function = self.process_first_message

    def process(self, message):
        if message == '/':
            self.session.send_to_client("Despliegue de snapshot cancelado.")
            self.finish_interaction()
        else:
            self.current_process_function(message)

    def process_first_message(self, message):
        self.show_world_snapshot_list()
        self.current_process_function = self.process_menu_option

    def process_menu_option(self, message):
        if message == '/':
            self.session.send_to_client('Cancelado.')
            self.finish_interaction()
            return
            
        try:
            index = int(message)
            if index < 0:
                raise ValueError
        except ValueError:
            self.session.send_to_client("Introduce un número")
            return

        world = self.session.user.room.world_state.get_world()

        snapshots = world.snapshots

        try:
            chosen_snapshot = snapshots[index]
        except IndexError:
            self.session.send_to_client("Introduce el número correspondiente a uno de los snapshots")
            return

        if chosen_snapshot is not None:
            world = self.session.user.room.world_state.get_world()
            self.deploy_snapshot(chosen_snapshot, world)
            self.session.send_to_client('{} desplegado. Puedes recuperar el mundo tal y como era antes del despliegue. Para hacerlo, despliega el snapshot "{}".'.format(chosen_snapshot.name, _backup_snapshot_name))
            self.finish_interaction()

    def show_world_snapshot_list(self):
        world = self.session.user.room.world_state.get_world()
        
        if not world.snapshots:
            self.session.send_to_client('Este mundo no tiene snapshots que desplegar.')
            self.finish_interaction()
            return

        message = '¿Qué snapshot quieres desplegar? ("/" para cancelar)\n'

        snapshots = world.snapshots

        for i, snapshot in enumerate(snapshots):
            message += ' {} - {}\n'.format(i, snapshot.name)

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


class PubishSnapshot(verb.Verb):
    command = 'publicar'
    permissions = verb.CREATOR

    def process(self, message):
        self.show_world_snapshot_list()
        self.process = self.process_menu_option

    def process_menu_option(self, message):
        if message == '/':
            self.session.send_to_client('Publicación de snapshot cancelada.')
            self.finish_interaction()
            return
            
        try:
            index = int(message)
            if index < 0:
                raise ValueError
        except ValueError:
            self.session.send_to_client("Introduce un número")
            return

        world = self.session.user.room.world_state.get_world()

        publishable_snapshots = list(filter(lambda s: s.public==False and s.name!=_backup_snapshot_name, world.snapshots))

        try:
            chosen_snapshot = publishable_snapshots[index]
        except IndexError:
            self.session.send_to_client("Introduce el número correspondiente a uno de los snapshots")
            return

        if chosen_snapshot is not None:
            chosen_snapshot.publish()
            self.session.send_to_client('Hecho, el snapshot ha sido publicado!')
            self.finish_interaction()

    def show_world_snapshot_list(self):
        world = self.session.user.room.world_state.get_world()
        publishable_snapshots = list(filter(lambda s: s.public==False and s.name!=_backup_snapshot_name, world.snapshots))

        if not publishable_snapshots:
            self.session.send_to_client('Este mundo no tiene snapshots que publicar.')
            self.finish_interaction()
            return
        
        message = '¿Qué snapshot quieres publicar? ("/" para cancelar)\n'
        
        if len(publishable_snapshots) == 0:
            message += 'No hay ningún snapshot sin publicar.\n'

        for i, snapshot in enumerate(publishable_snapshots):
            message += ' {} - {}\n'.format(i, snapshot.name)

        self.session.send_to_client(message)


class UnpubishSnapshot(verb.Verb):
    command = 'despublicar'
    permissions = verb.CREATOR

    def process(self, message):
        self.show_published_snapshot_list()
        self.process = self.process_menu_option

    def process_menu_option(self, message):
        if message == '/':
            self.session.send_to_client('Cancelado.')
            self.finish_interaction()
            return
            
        try:
            index = int(message)
            if index < 0:
                raise ValueError
        except ValueError:
            self.session.send_to_client("Introduce un número")
            return

        your_worlds = entities.World.objects(creator=self.session.user)
        your_public_snapshots = [(snapshot, world) for world in your_worlds for snapshot in world.snapshots if snapshot.public]

        try:
            chosen_snapshot = your_public_snapshots[index][0]
        except IndexError:
            self.session.send_to_client("Introduce el número correspondiente a uno de los snapshots")
            return
        
        if chosen_snapshot is not None:
            chosen_snapshot.unpublish()
            self.session.send_to_client('Hecho, el snapshot ha sido des-publicado!')
            self.finish_interaction()

    def show_published_snapshot_list(self):
        your_worlds = entities.World.objects(creator=self.session.user)
        your_public_snapshots = [(snapshot, world) for world in your_worlds for snapshot in world.snapshots if snapshot.public]

        if len(your_public_snapshots) == 0:
            self.session.send_to_client('No hay ningún snapshot publicado en tus mundos.')
            self.finish_interaction()
            return

        message = 'Estas son las snapshots publicadas de tus mundos.\n¿Cuál quieres despublicar? ("/" para cancelar)\n'

        for i, (snapshot, world) in enumerate(your_public_snapshots):
            message += ' {} - {: <24} Mundo: {}\n'.format(i, snapshot.name, world.name)

        self.session.send_to_client(message)


class DeleteSnapshot(verb.Verb):
    command = 'borrarsnapshot'
    permissions = verb.CREATOR

    def process(self, message):
        self.show_world_snapshot_list()
        self.process = self.process_menu_option

    def show_world_snapshot_list(self):
        world = self.session.user.room.world_state.get_world()
        self.deletable_snapshots = list(filter(lambda s: s.public==False, world.snapshots))

        if not self.deletable_snapshots:
            self.session.send_to_client('Este mundo no tiene snapshots que eliminar. Si quieres eliminar un snapshot público, primero despubícalo.')
            self.finish_interaction()
            return
        
        message = '¿Qué snapshot quieres eliminar? (ES IRREVERSIBLE)\nSi quieres eliminar un snapshot público, primero despublícalo\n'

        for i, snapshot in enumerate(self.deletable_snapshots):
            message += ' {} - {}\n'.format(i, snapshot.name)
        message += '\n("/" para cancelar)'

        self.session.send_to_client(message)

    def process_menu_option(self, message):
        if message == '/':
            self.session.send_to_client('Cancelado.')
            self.finish_interaction()
            return

        try:
            index = int(message)
            if index < 0:
                raise ValueError
        except ValueError:
            self.session.send_to_client("Introduce un número")
            return

        try:
            chosen_snapshot = self.deletable_snapshots[index]
        except IndexError:
            self.session.send_to_client("Introduce el número correspondiente a uno de los snapshots")
            return

        chosen_snapshot.delete()
        self.session.send_to_client('Hecho, el snapshot ha sido borrado!')
        self.finish_interaction()
