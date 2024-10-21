#!/usr/bin/env python3

"""
Claim Module

This module contains the Claim class and its subclasses:
- Suggestion: Represents a suggestion made by a player
- Accusation: Represents an accusation made by a player

Author: Stephen "Christian" Kocsis
Date: 2024-10-19
"""
from abc import ABC, abstractmethod

class Claim(ABC):

    def __init__(self, character, weapon, room):
        self.character = character
        self.weapon = weapon
        self.room = room

    @abstractmethod
    def make_string(self):
        pass

    @abstractmethod
    def dict(self):
        pass

class Suggestion(Claim):
    def make_string(self):
        return f"I suggest it was {self.character.value} with the {self.weapon.get_name()} in the {self.room.value}"

    def dict(self):
        data = {
            "suggestion": {
                "character": self.character.name,
                "weapon": self.weapon.get_name_enum().name,
                "room": self.room.name
            }
        }

        return data

class Accuse(Claim):
    def make_string(self):
        return f"I accuse {self.character.value} with the {self.weapon.get_name()} in the {self.room.value}"

    def dict(self):
        data = {
            "accusation": {
                "character": self.character.name,
                "weapon": self.weapon.get_name_enum().name,
                "room": self.room.name
            }
        }

        return data