from . import verb
from .. import entities


class MakeEditor(verb.Verb):
    command = 'hacereditor '
    permissions = verb.CREATOR

    def process(self, message):
        target_user_name = message[len(self.command):]
        target_user = next(entities.User.objects(name=target_user_name), None)
        world = self.session.user.room.world_state.get_world()

        if target_user is not None:
            world.add_editor(target_user)
            self.session.send_to_client('Hecho, ahora {} es editor de {}'.format(target_user.name, world.name))
            self.session.send_to_user(target_user, 'Te acaban de hacer editor')
        else:
            self.session.send_to_client('Ese usuario no existe.')

        self.finish_interaction()


class RemoveEditor(verb.Verb):
    command = 'quitareditor '
    permissions = verb.CREATOR

    def process(self, message):
        target_user_name = message[len(self.command):]
        target_user = next(entities.User.objects(name=target_user_name), None)
        world = self.session.user.room.world_state.get_world()

        if target_user is not None:
            if target_user in world.editors:
                world.remove_editor(target_user)
                self.session.send_to_client('Hecho, ahora {} ya no es editor de {}'.format(target_user.name, world.name))
                self.session.send_to_user(target_user, 'Te acaban de quitar como editor')
            else:
                self.session.send_to_client('No puedes quitar permisos a ese usuario porque no los tiene.')
        else:
            self.session.send_to_client('Ese usuario no existe.')

        self.finish_interaction()
        

