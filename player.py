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
        return f"{self.name} : {self.character.name}"

    def set_position(self, x, y):
        """Set the player's position."""
        self.position = (x, y)

    def get_position(self):
        """Get the player's current position."""
        return self.position

    def add_cards(self, cards):
        """Add cards to the player's hand."""
        for card in cards:
            card.player = self
        self.cards.extend(cards)

    def get_cards(self):
        """Get the player's cards."""
        return self.cards

    def add_note(self, note):
        """Add a note to the player's notes."""
        self.notes += note

    def _get_cards_string(self):
        """Return a list of dictionaries representing each card."""
        return [card.dict() for card in self.cards]

    def dict(self):
        """Return a dictionary representation of the player."""
        data = {
            "name": self.name,
            "character": self.character.value,
            "position": {"x": self.position[0], "y": self.position[1]},
            "cards": self._get_cards_string(),
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
        """Return the default position for the character."""
        return 0, 0
