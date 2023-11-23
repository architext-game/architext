class CantDeleteRoomWithPlayers(Exception):
    pass

class CantDeleteStartingRoom(Exception):
    pass

class CantUseClosedExit(Exception):
    pass

class CantUseExitInAnotherRoom(Exception):
    pass