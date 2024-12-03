#!/usr/bin/env python3

"""
Claim Module

This module contains the Claim class and its subclasses:
- Suggestion: Represents a suggestion made by a player
- Accusation: Represents an accusation made by a player

Author: Nick Weiner & Stephen "Christian" Kocsis
Date: 2024-10-30
"""
from abc import ABC, abstractmethod

from datetime import datetime
import time

class Claim(ABC):

    def __init__(self, player, character, weaponName, room):
        self.player = player
        self.character = character
        self.weaponName = weaponName
        self.room = room
        self.timestamp = int(time.time())

    @abstractmethod
    def make_string(self):
        pass

    @abstractmethod
    def dict(self):
        pass

    def get_subjects(self):
        return self.character, self.weaponName, self.room

    def format_dict(self, subject, disprover_name):
        temp_dict = self.dict()
        if subject is not None:
            temp_dict['disproving_subject'] = subject.value

        if disprover_name is not None:
            temp_dict['disprover'] = disprover_name

        return temp_dict

class Suggestion(Claim):
    def make_string(self):
        return f"{self.player.name} suggests it was {self.character.value} with the {self.weaponName.value} in the {self.room.value}"

    def dict(self):
        data = {
            "suggestion": {
                "player": self.player.get_name(),
                "character": self.character.name,
                "weapon": self.weaponName.value,
                "room": self.room.name,
                "timestamp": self.timestamp
            }
        }

        return data

class Accusation(Claim):
    def make_string(self):
        return f"{self.player.name} accuses {self.character.value} with the {self.weaponName.value} in the {self.room.value}"

    def dict(self):
        data = {
            "accusation": {
                "player": self.player.get_name(),
                "character": self.character.name,
                "weapon": self.weaponName.value,
                "room": self.room.name,
                "timestamp": self.timestamp
            }
        }

        return data
