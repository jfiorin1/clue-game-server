#!/usr/bin/env python3
"""
Player Module

This module contains the Weapon Class and the WeaponName Enum
Author: Nick Weiner
Date: 2024-10-19
"""
from enum import Enum
from room import Room

class Weapon:

    def __init__(self, name, room: Room = None):
        self.name = name
        self.room = room

    def __str__(self):
        return self.name + " " + self.room

    def get_name(self):
        return self.name.value

    def get_name_enum(self):
        return self.name

    def get_room(self):
        return self.room

    def set_room(self, room):
        self.room = room

    @staticmethod
    def get_unassigned_weapons():
        return [Weapon(name, None) for name in WeaponName]

    def dict(self):
        if self.room is None:
            coordinates = None
        else:
            coordinates = self.room.coordinates

        data = {
            "name": self.get_name(),
            "room": coordinates
        }
        return data

class WeaponName(Enum):
    CANDLESTICK = "Candlestick"
    DAGGER = "Dagger"
    LEAD_PIPE = "Lead Pipe"
    REVOLVER = "Revolver"
    ROPE = "Rope"
    WRENCH = "Wrench"