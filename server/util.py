import logging
import entities
import os


def possible_meanings(partial_string, list_of_options):
    if partial_string in list_of_options:
        return [string for string in list_of_options if partial_string == string]
    else:
        return [string for string in list_of_options if partial_string in string]


def get_items_in_world():
    items_in_world = []
    for room in entities.Room.objects():
        items_in_world = items_in_world + room.items
    return items_in_world

def name_globaly_free(session, item_name, ignore_item=None):
    if item_name in [takable_item.name for takable_item in get_items_in_world() if takable_item != ignore_item and takable_item.visible=='takable']:
        session.send_to_client("En este mundo hay un objeto cogible con ese nombre. Debes elegir otro.")
        return False
    
    return True


def valid_item_or_exit_name(session, item_name, ignore_item=None, local_room=None):
    '''Returns true if the item name is valid to be assigned to a not Takable item or an exit. Otherwise, sends an error message to the client and returns False.
    For takable items, further checks are necessary. Specifically, the Takable item should be unique across all items and exits.'''
    if local_room is None:
        local_room = session.user.room
    
    if not item_name:
        session.send_to_client("El nombre no puede estar vacío. Prueba otra vez.")
        return False

    if item_name in [item.name for item in local_room.items if item != ignore_item]:
        session.send_to_client("Ya hay un objeto con ese nombre en esta sala. Prueba a ponerle otro nombre")
        return False

    if item_name in [exit.name for exit in local_room.exits if exit != ignore_item]:
        session.send_to_client("En esta sala hay un salida con ese nombre. Tienes que elegir otro diferente.")
        return False
    
    if not name_globaly_free(session, item_name, ignore_item=ignore_item):
        return False
    
    return True


def valid_takable_item_name(session, item_name, ignore_item=None):
    '''Returns true if the item name is valid to be assigned to a Takable item. Otherwise, sends an error message to the client and returns False.'''
    if not valid_item_or_exit_name(session, item_name, ignore_item=ignore_item):
        return False

    if item_name in [item.name for item in get_items_in_world() if item != ignore_item]:
        session.send_to_client("En este mundo hay un objeto con este nombre. Debes elegir otro, puesto que los nombres de los objetos cogibles deben ser únicos.")
        return False

    if item_name in [exit.name for exit in get_items_in_world() if exit != ignore_item]:
        session.send_to_client("En este mundo hay una salida con este nombre. Debes elegir otro, puesto que los nombres de los objetos cogibles deben ser únicos.")
        return False

    return True


def setup_logger(logger_name, log_file, console=False, level=logging.INFO):
    """Sets up a logger that can be used across all modules.
    Example:
        setup_logger('log1', "logs.txt")  # Sets up the logger
        logger_1 = logging.getLogger('log1')  # Gets the logger (works from anywhere)
        logger_1.info('Some info to log')  # logs something
    """
    if not os.path.exists('logs'):
        os.makedirs('logs')

# handler = logging.handlers.RotatingFileHandler(
#              LOG_FILENAME, maxBytes=20, backupCount=5)

    logger = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(asctime)s: %(message)s')
    fileHandler = logging.FileHandler(os.getcwd() + '/logs/' + log_file, 'a', 'utf-8')
    fileHandler.setFormatter(formatter)
    if console:
        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(formatter)
        logger.addHandler(streamHandler)  

    logger.setLevel(level)
    logger.addHandler(fileHandler)
      

    return logger


