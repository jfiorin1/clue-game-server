#!/usr/bin/env python3
"""
Player Module

This module contains the Weapon Class and the WeaponName Enum
Author: Nick Weiner
Date: 2024-10-19
"""
import json
from enum import Enum

class Weapon:

    def __init__(self, name, room):
        self.name = name
        self.room = room

    def __str__(self):
        return self.name + " " + self.room

    def get_name(self):
        return self.name.value

    @staticmethod
    def get_unassigned_weapons():
        return [Weapon(name, None) for name in WeaponName]

    def json_serialize(self):
        data = {
            "name": self.name,
            "room": self.room.coordinates
        }
        return json.dumps(data)

class WeaponName(Enum):
    CANDLESTICK = "Candlestick"
    DAGGER = "Dagger"
    LEAD_PIPE = "Lead Pipe"
    REVOLVER = "Revolver"
    ROPE = "Rope"
    WRENCH = "Wrench"