from . import verb
from .. import entities
from .. import util
import functools
import architext.strings as strings

class PlaceItem(verb.Verb):
    command = _("spawn")
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
            self.session.send_to_client(_("There is no item with the id {item_id} in this world.").format(item_id=provided_item_id))
            self.list_your_saved_messages()
        elif saved_item == "many":
            raise Exception("There was more than one item with the same id.")
        else:
            item_to_place = saved_item.clone()
            try:
                item_to_place.put_in_room(self.session.user.room)
            except entities.RoomNameClash:
                self.session.send_to_client(_('The item could not be spawned: there is already an item or exit with that name in this room.'))
            except entities.TakableItemNameClash:
                self.session.send_to_client(_('The item could not be spawned: there is a takable item with that name in this world (takable items need an unique name).'))
            except entities.NameNotGloballyUnique:
                self.session.send_to_client(_('The item could not be spawned: it is a takable item, and there is already an item with that name in this world.'))   
            else:
                self.session.send_to_client(_('You spawned "{item_name}" in this world.').format(item_name=item_to_place.name))

    def list_your_saved_messages(self):
        saved_items = entities.Item.objects(saved_in=self.session.user.room.world_state)
        if len(saved_items) > 0:
            saved_item_ids = ["'{}'".format(item.item_id) for item in saved_items]
            saved_item_list = functools.reduce(lambda a, b: '{}\n{}'.format(a,b), saved_item_ids)
            self.session.send_to_client(_('Saved items in this world:\n{saved_item_list}').format(saved_item_list=saved_item_list))
        else:
            self.session.send_to_client(_("There are no saved items in this world."))


class SaveItem(verb.Verb):
    command = _('save ')
    permissions = verb.PRIVILEGED

    def process(self, message):
        item_name = message[len(self.command):]
        selected_item = util.name_to_entity(self.session, item_name, substr_match=["room_items", "inventory"])

        if selected_item == "many":
            self.session.send_to_client(strings.many_found)
        elif selected_item is None:
            self.session.send_to_client(strings.not_found)            
        else:
            snapshot = self.session.user.save_item(selected_item)
            self.session.send_to_client(_('{item_name} has been saved as {item_id}. To spawn it, use "spawn {item_id}". You can also edit and add verbs to it.').format(item_name=snapshot.name, item_id=snapshot.item_id))
            
        self.finish_interaction()

        
