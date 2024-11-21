#!/usr/bin/env python3
"""
Player Module

This module contains the Player Class, the CharacterHandle Class, and the ClueCharacter Enum
Author: Nick Weiner
Date: 2024-10-19
"""

from enum import Enum

from playerTurnManager import PlayerTurnManager
from claim import Suggestion, Accusation

class Player:
    def __init__(self, name, character, gameManager):
        self.name = name
        self.characterHandler = CharacterHandler(character)
        self.turn = PlayerTurnManager()

        self.gameManager = gameManager

        self.cards = []
        self.notes = ""
        self.is_active = True
        self.is_eliminated = False


    def __str__(self):
        return self.name + " : " + self.characterHandler.character.name

    def get_name(self):
        return self.name

    def set_position(self, x, y):
        self.characterHandler.set_position(x, y)

    def get_position(self):
        return self.characterHandler.position

    def get_turn_manager(self):
        return self.turn

    def add_cards(self, cards):
        for card in cards:
            card.player = self
        self.cards += cards

    def has_card(self, subject):
        for card in self.cards:
            if card.subject == subject:
                return True
        return False

    def get_cards(self):
        return self.cards

    def add_note(self, note):
        self.notes += note

    def eliminate(self):
        self.is_eliminated = True

    def _get_cards_dict(self):
        return [card.dict() for card in self.cards]

    def dict(self):
        data = {
            "name": self.name,
            "character": self.characterHandler.character.value,
            "position": {
                "x": self.characterHandler.position[0],
                "y": self.characterHandler.position[1]
            },
            "cards": self._get_cards_dict(),
            "notes": self.notes,
            "is_active": self.is_active,
            "is_eliminated": self.is_eliminated
        }

        return data

class CharacterHandler:
    def __init__(self, character):
        self.character = character
        self.position = character.get_default_position()

    def set_position(self, x, y):
        self.position = (x, y)

class ClueCharacter(Enum):
    MRS_WHITE = "Mrs. White"
    MRS_PEACOCK = "Mrs. Peacock"
    PROFESSOR_PLUM = "Professor Plum"
    COLONEL_MUSTARD = "Colonel Mustard"
    MISS_SCARLETT = "Miss Scarlett"
    REVEREND_GREEN = "Reverend Green"

    def get_default_position(self):
        match self:
            case ClueCharacter.MRS_WHITE:
                return 4, 6
            case ClueCharacter.MRS_PEACOCK:
                return 0, 4
            case ClueCharacter.PROFESSOR_PLUM:
                return 0, 2
            case ClueCharacter.COLONEL_MUSTARD:
                return 6, 2
            case ClueCharacter.MISS_SCARLETT:
                return 4, 0
            case ClueCharacter.REVEREND_GREEN:
                return 2, 6
