##################################################
## {Description}
##################################################
## Author: Nick Weiner
##################################################
import json
from abc import ABC, abstractmethod

class Claim(ABC):

    def __init__(self, character, weapon, room):
        self.character = character
        self.weapon = weapon
        self.room = room

    @abstractmethod
    def make_string(self):
        pass

    def json_serialize(self):
        data = {
            "character": self.character,
            "weapon": self.weapon,
            "room": self.room
        }

        return json.dumps(data)

class Suggestion(Claim):
    def make_string(self):
        return f"I suggest it was {self.character.name} with the {self.weapon} in the {self.room}"

class Accuse(Claim):
    def make_string(self):
        return f"I accuse {self.character.name} with the {self.weapon} in the {self.room}"