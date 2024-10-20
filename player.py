##################################################
## {Description}
##################################################
## Author: Nick Weiner
##################################################

from enum import Enum
import json

class Player:
    def __init__(self, name, character):
        self.name = name
        self.character = character
        self.position = character.get_default_position

        self.cards = []
        self.accusations_made = []
        self.suggestions_made = []
        self.notes = ""
        self.is_active = True


    def __str__(self):
        return self.name + " : " + self.character.name

    def set_position(self, x, y):
        self.position = (x, y)

    def add_card(self, card):
        self.cards.append(card)

    def add_suggestion(self, suggestion):
        self.suggestions_made.append(suggestion)

    def add_accusation(self, accusation):
        self.accusations_made.append(accusation)

    def add_note(self, note):
        self.notes += note

    def get_cards_string(self):
        return [card.json_serialize() for card in self.cards]

    def get_accusations_string(self):
        return [accusation.json_serialize() for accusation in self.accusations_made]

    def get_suggestions_string(self):
        return [suggestion.json_serialize() for suggestion in self.suggestions_made]

    def json_serialize(self):
        data = {
            "name": self.name,
            "character": self.character.name,
            "position": self.position,
            "cards": self.get_cards_string(),
            "accusations": self.get_accusations_string(),
            "suggestions": self.get_suggestions_string(),
            "notes": self.notes,
            "is_active": self.is_active
        }

        return json.dumps(data)


class ClueCharacter(Enum):
    MRS_WHITE = "Mrs. White"
    MRS_PEACOCK = "Mrs. Peacock"
    PROFESSOR_PLUM = "Professor Plum"
    COLONEL_MUSTARD = "Colonel Mustard"
    MISS_SCARLETT = "Miss Scarlett"
    REVEREND_GREEN = "Reverend Green"

    def get_default_position(self):
        raise NotImplementedError()