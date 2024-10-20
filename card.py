##################################################
## {Description}
##################################################
## Author: Nick Weiner
##################################################
import json
from abc import ABC, abstractmethod

class Card(ABC):
    def __init__(self, player):
        self.player = player

    @abstractmethod
    def json_serialize(self):
        pass

class CharacterCard(Card):
    def __init__(self, player, character):
        super().__init__(player)
        self.character = character

    def json_serialize(self):
        data = {
            "card": {
                "character": self.character.name
            }
        }

        return json.dumps(data)

class WeaponCard(Card):
    def __init__(self, player, weapon):
        super().__init__(player)
        self.weapon = weapon

    def json_serialize(self):
        data = {
            "card": {
                "weapon": self.weapon.get_name()
            }
        }

        return json.dumps(data)

class RoomCard(Card):
    def __init__(self, player, room):
        super().__init__(player)
        self.room = room

    def json_serialize(self):
        data = {
            "card": {
                "room": self.room.name
            }
        }