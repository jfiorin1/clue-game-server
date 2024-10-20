##################################################
## {Description}
##################################################
## Author: Nick Weiner
##################################################

from enum import Enum

class Room(Enum):
    STUDY = "Study"
    HALL = "Hall"
    LOUNGE = "Lounge"
    LIBRARY = "Library"
    BILLIARD = "Billiard Room"
    DINING = "Dining Room"
    CONSERVATORY = "Conservatory"
    BALLROOM = "Ballroom"
    KITCHEN = "Kitchen"

    _room_coordinates = {
        STUDY: (0, 0),
        HALL: (2, 0),
        LOUNGE: (4, 0),
        LIBRARY: (0, 2),
        BILLIARD: (2, 2),
        DINING: (4, 2),
        CONSERVATORY: (0, 4),
        BALLROOM: (2, 4),
        KITCHEN: (4, 4)
    }

    @property
    def coordinates(self):
        return Room._room_coordinates[self]