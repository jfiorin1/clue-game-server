#!/usr/bin/env python3

"""
Claim Module

This module contains the Claim class and its subclasses:
- Suggestion: Represents a suggestion made by a player
- Accusation: Represents an accusation made by a player

Author: Stephen "Christian" Kocsis
Date: 2024-10-30
"""
from abc import ABC, abstractmethod

from datetime import datetime

class Claim(ABC):

    def __init__(self, player, character, weaponName, room):
        self.player = player
        self.character = character
        self.weaponName = weaponName
        self.room = room
        self.timestamp = datetime.now()

    @abstractmethod
    def make_string(self):
        pass

    @abstractmethod
    def dict(self):
        pass
      
    @abstractmethod
    def get_info(self):
        pass
      
    @abstractmethod
    def validate(self):
        pass

class Suggestion(Claim):
    def make_string(self):
        return f"I suggest it was {self.character.value} with the {self.weaponName.value} in the {self.room.value}"

    def dict(self):
        data = {
            "suggestion": {
                "player": self.player.get_name(),
                "character": self.character.name,
                "weapon": self.weaponName.value,
                "room": self.room.name
            }
        }

        return data

class Accusation(Claim):
    def make_string(self):
        return f"I accuse {self.character.value} with the {self.weaponName.value} in the {self.room.value}"

    def dict(self):
        data = {
            "accusation": {
                "player": self.player.get_name(),
                "character": self.character.name,
                "weapon": self.weaponName.value,
                "room": self.room.name
            }
        }

        return data
