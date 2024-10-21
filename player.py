#!/usr/bin/env python3
"""
Player Module

This module contains the Player Class and the ClueCharacter Enum
Author: Nick Weiner
Date: 2024-10-19
"""

from enum import Enum

from playerTurnManager import PlayerTurnManager

class Player:
    def __init__(self, name, character):
        self.name = name
        self.character = character
        self.position = character.get_default_position()
        self.turn = PlayerTurnManager()

        self.cards = []
        self.notes = ""
        self.is_active = True


    def __str__(self):
        return self.name + " : " + self.character.name

    def set_position(self, x, y):
        self.position = (x, y)

    def get_position(self):
        return self.position

    def add_cards(self, cards):
        for card in cards:
            card.player = self
        self.cards += cards

    def get_cards(self):
        return self.cards

    def add_note(self, note):
        self.notes += note

    def _get_cards_string(self):
        return [card.dict() for card in self.cards]

    def dict(self):
        data = {
            "name": self.name,
            "character": self.character.value,
            "position": {
                "x": self.position[0],
                "y": self.position[1]
            },
            "cards": self._get_cards_string(), # could be a future issue, not sure how nesting dumps works
            "notes": self.notes,
            "is_active": self.is_active
        }

        return data


class ClueCharacter(Enum):
    MRS_WHITE = "Mrs. White"
    MRS_PEACOCK = "Mrs. Peacock"
    PROFESSOR_PLUM = "Professor Plum"
    COLONEL_MUSTARD = "Colonel Mustard"
    MISS_SCARLETT = "Miss Scarlett"
    REVEREND_GREEN = "Reverend Green"

    def get_default_position(self):
        return 0, 0