#!/usr/bin/env python3

"""
Claim Module

This module contains the Claim class and its subclasses:
- Suggestion: Represents a suggestion made by a player
- Accusation: Represents an accusation made by a player

Author: Stephen "Christian" Kocsis
Date: 2024-10-19
"""
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

    @abstractmethod
    def json_serialize(self):
        pass

class Suggestion(Claim):
    def make_string(self):
        return f"I suggest it was {self.character.name} with the {self.weapon} in the {self.room}"

    def json_serialize(self):
        data = {
            "suggestion": {
                "character": self.character,
                "weapon": self.weapon,
                "room": self.room
            }
        }

        return json.dumps(data)

class Accuse(Claim):
    def make_string(self):
        return f"I accuse {self.character.name} with the {self.weapon} in the {self.room}"

    def json_serialize(self):
        data = {
            "accusation": {
                "character": self.character,
                "weapon": self.weapon,
                "room": self.room
            }
        }

        return json.dumps(data)