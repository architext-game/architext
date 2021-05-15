from . import verb
from .. import entities
from .. import util
import functools

class PlaceItem(verb.Verb):
    command = "colocar"
    permissions = verb.PRIVILEGED

    def process(self, message):
        if message.startswith(self.command+' '):
            id_of_item_to_place = message[len(self.command)+1:]
            self.place(id_of_item_to_place)
        else:
            self.list_your_saved_messages()
        self.finish_interaction()

    def place(self, provided_item_id):
        saved_item = util.name_to_entity(self.session, provided_item_id, loose_match=["saved_items"])

        if saved_item is None:
            self.session.send_to_client("No hay ningún objeto guardado con el identificador '{}' en este mundo.".format(provided_item_id))
            self.list_your_saved_messages()
        elif saved_item == "many":
            raise Exception("There was more than one item with the same id.")
        else:
            item_to_place = saved_item.clone()
            try:
                item_to_place.put_in_room(self.session.user.room)
            except entities.RoomNameClash:
                self.session.send_to_client("En esta sala ya hay un objeto o salida con ese nombre.")
            except entities.TakableItemNameClash:
                self.session.send_to_client("El objeto no se puede colocar porque en el mundo hay un objeto cogible con ese nombre.")
            except entities.NameNotGloballyUnique:
                self.session.send_to_client("El objeto no se puede colocar, porque es cogible y ya hay un objeto con ese nombre en este mundo.")   
            else:
                self.session.send_to_client(f'Has colocado "{item_to_place.name}" en esta sala.')

    def list_your_saved_messages(self):
        saved_items = entities.Item.objects(saved_in=self.session.user.room.world_state)
        if len(saved_items) > 0:
            saved_item_ids = ["'{}'".format(item.item_id) for item in saved_items]
            saved_item_list = functools.reduce(lambda a, b: '{}\n{}'.format(a,b), saved_item_ids)
            self.session.send_to_client('Objetos guardados en este mundo:\n{}'.format(saved_item_list))
        else:
            self.session.send_to_client("No has guardado ningún objeto en este mundo.")


class SaveItem(verb.Verb):
    command = 'guardar '
    permissions = verb.PRIVILEGED

    def process(self, message):
        message = message[len(self.command):]
        selected_item = util.name_to_entity(self.session, item_name, substr_match=["room_items", "inventory"])

        if selected_item == "many":
            self.session.send_to_client("Hay más de un objeto con un nombre similar a ese. Sé más expecífico.")
        elif selected_item is None:
            self.session.send_to_client("No existe ese objeto en esta habitación.")            
        else:
            snapshot = self.session.user.save_item(selected_item)
            self.session.send_to_client(f"Se ha guardado {selected_item.name} como {snapshot.item_id}. Para colocarlo escribe: colocar {snapshot.item_id}")
            
        self.finish_interaction()

        
