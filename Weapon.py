##################################################
## {Description}
##################################################
## Author: Nick Weiner
##################################################

from enum import Enum

class Weapon:

    def __init__(self, name, room):
        self.name = name
        self.room = room

    def __str__(self):
        return self.name + " " + self.room

    def get_name(self):
        return self.name.value

    class WeaponName(Enum):
        CANDLESTICK = "Candlestick"
        DAGGER = "Dagger"
        LEAD_PIPE = "Lead Pipe"
        REVOLVER = "Revolver"
        ROPE = "Rope"
        WRENCH = "Wrench"