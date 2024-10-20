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
import json
from abc import ABC, abstractmethod

class Card(ABC):
    def __init__(self, player):
        self.player = player

    @abstractmethod
    def json_serialize(self):
        pass

class CharacterCard(Card):
    def __init__(self, player, character):
        super().__init__(player)
        self.character = character

    def json_serialize(self):
        data = {
            "character_card":  self.character.name
        }

        return json.dumps(data)

class WeaponCard(Card):
    def __init__(self, player, weapon):
        super().__init__(player)
        self.weapon = weapon

    def json_serialize(self):
        data = {
            "weapon_card":  self.weapon.get_name()
        }

        return json.dumps(data)

class RoomCard(Card):
    def __init__(self, player, room):
        super().__init__(player)
        self.room = room

    def json_serialize(self):
        data = {
            "room_card": self.room.name
        }