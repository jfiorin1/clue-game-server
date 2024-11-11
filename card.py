#!/usr/bin/env python3

"""
Card Module

This module contains the Card class and its subclasses:
- CharacterCard: Represents a character in the game
- Weapon: Represents a weapon in the game
- Room: Represents a room in the game

Author: Stephen "Christian" Kocsis
Date: 2024-10-30
"""
from abc import ABC, abstractmethod
import json


class Card(ABC):
    def __init__(self, player=None):
        self.player = player

    @abstractmethod
    def dict(self):
        pass

    @abstractmethod
    def deserialize(self, jstring):
        pass

    @abstractmethod
    def get_subject(self):
        pass

class CharacterCard(Card):
    def __init__(self, character):
        super().__init__()
        self.character = character

    def dict(self):
        data = {
            "character_card":  self.character.value
        }
        return data

    def deserialize(self, jstring):
        data = json.loads(jstring)
        self.character.value = data["character_card"]

    def get_subject(self):
        return self.character

class WeaponCard(Card):
    def __init__(self, weaponName):
        super().__init__()
        self.weaponName = weaponName

    def dict(self):
        data = {
            "weapon_card":  self.weaponName.value
        }
        return data

    def deserialize(self, jstring):
        data = json.loads(jstring)
        self.weaponName.value = data["weapon_card"]

    def get_subject(self):
        return self.weaponName

class RoomCard(Card):
    def __init__(self, room):
        super().__init__()
        self.room = room

    def dict(self):
        data = {
            "room_card": self.room.value
        }
        return data

    def deserialize(self, jstring):
        data = json.loads(jstring)
        self.room.value = data["room_card"]

    def get_subject(self):
        return self.room
