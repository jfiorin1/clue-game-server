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


class Card(ABC):
    def __init__(self, player=None):
        self.player = player  # Player the card belongs to

    @abstractmethod
    def dict(self):
        pass

    @abstractmethod
    def get_subject(self):
        pass

    def __str__(self):
        return f"{self.__class__.__name__} - {self.get_subject()}"


class CharacterCard(Card):
    def __init__(self, character):
        super().__init__()
        self.character = character

    def dict(self):
        return {
            "character_card": self.character.value
        }

    def get_subject(self):
        return self.character

    def __str__(self):
        return f"Character: {self.character}"


class WeaponCard(Card):
    def __init__(self, weapon):
        super().__init__()
        self.weapon = weapon

    def dict(self):
        return {
            "weapon_card": self.weapon.get_name()
        }

    def get_subject(self):
        return self.weapon

    def __str__(self):
        return f"Weapon: {self.weapon.get_name()}"


class RoomCard(Card):
    def __init__(self, room):
        super().__init__()
        self.room = room

    def dict(self):
        return {
            "room_card": self.room.value
        }

    def get_subject(self):
        return self.room

    def __str__(self):
        return f"Room: {self.room}"
        
