#!/usr/bin/env python3

"""
Card Module

This module contains the Card class and its subclasses:
- CharacterCard: Represents a character in the game
- Weapon: Represents a weapon in the game
- Room: Represents a room in the game

Author: Stephen "Christian" Kocsis
Date: 2024-10-19
"""
from abc import ABC, abstractmethod

class Card(ABC):
    def __init__(self, player=None):
        self.player = player

    @abstractmethod
    def dict(self):
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

    def get_subject(self):
        return self.character

class WeaponCard(Card):
    def __init__(self, weapon):
        super().__init__()
        self.weapon = weapon

    def dict(self):
        data = {
            "weapon_card":  self.weapon.get_name()
        }
        return data

    def get_subject(self):
        return self.weapon

class RoomCard(Card):
    def __init__(self, room):
        super().__init__()
        self.room = room

    def dict(self):
        data = {
            "room_card": self.room.value
        }
        return data

    def get_subject(self):
        return self.room