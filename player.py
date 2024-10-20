#!/usr/bin/env python3
"""
Player Module

This module contains the Player Class and the ClueCharacter Enum
Author: Nick Weiner
Date: 2024-10-19
"""

from enum import Enum
import json

class Player:
    def __init__(self, name, character):
        self.name = name
        self.character = character
        self.position = character.get_default_position

        self.cards = []
        self.notes = ""
        self.is_active = True


    def __str__(self):
        return self.name + " : " + self.character.name

    def set_position(self, x, y):
        self.position = (x, y)

    def add_card(self, card):
        self.cards.append(card)

    def add_note(self, note):
        self.notes += note

    def get_cards_string(self):
        return [card.json_serialize() for card in self.cards]

    def json_serialize(self):
        data = {
            "name": self.name,
            "character": self.character.name,
            "position": self.position,
            "cards": self.get_cards_string(), # could be a future issue, not sure how nesting dumps works
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