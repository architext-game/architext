from .verb import Verb
from .. import entities
import functools

class PlaceItem(Verb):
    command = "colocar"

    def process(self, message):
        if message.startswith(self.command+' '):
            id_of_item_to_place = message[len(self.command)+1:]
            self.place(id_of_item_to_place)
        else:
            self.list_your_saved_messages()
        self.finish_interaction()

    def place(self, provided_item_id):
        querry = entities.Item.objects(item_id=provided_item_id, room=None)

        if len(querry) == 0:
            self.session.send_to_client("No hay ningún objeto guardado con el identificador '{}'.".format(provided_item_id))
            self.list_your_saved_messages()
        elif len(querry) == 1:
            selected_item_snapshot = querry[0]
            item_to_place = selected_item_snapshot.clone()
            try:
                item_to_place.put_in_room(self.session.user.room)
            except entities.RoomNameClash:
                self.session.send_to_client("En esta sala ya hay un objeto o salida con ese nombre.")
            except entities.TakableItemNameClash:
                self.session.send_to_client("El objeto no se puede colocar porque en el mundo hay un objeto cogible con ese nombre.")
            except entities.NameNotGloballyUnique:
                self.session.send_to_client("El objeto no se puede colocar, porque es cogible y ya hay un objeto con ese nombre en este mundo.")   
            else:
                self.session.send_to_client("Hecho!")
        else:
            raise Exception("There was more than one item with the same id!")

    def list_your_saved_messages(self):
        if self.session.user.saved_items != []:
            saved_item_ids = ["'{}'".format(item.item_id) for item in self.session.user.saved_items]
            saved_item_list = functools.reduce(lambda a, b: '{}\n{}'.format(a,b), saved_item_ids)
            self.session.send_to_client('Estos son los objetos que has guardado:\n{}'.format(saved_item_list))
        else:
            self.session.send_to_client("No has guardado ningún objeto.")


class SaveItem(Verb):
    command = 'guardar '

    def process(self, message):
        message = message[len(self.command):]
        selected_item = next(filter(lambda i: i.name==message, self.session.user.room.items), None)
        if selected_item is not None:
            snapshot = self.session.user.save_item(selected_item)
            self.session.send_to_client("Se ha guardado {} como {}. Para colocarlo escribe: colocar {}".format(selected_item.name, snapshot.item_id, snapshot.item_id))
        else:
            self.session.send_to_client("No existe ese objeto en esta habitación.")
        self.finish_interaction()

        
