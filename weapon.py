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

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def get_name(self):
        return self.name.value

    def get_name_enum(self):
        return self.name

    @staticmethod
    def generate_unassigned_weapons():
        return [Weapon(name) for name in WeaponName]

    def dict(self):
        data = {
            "name": self.get_name(),
        }
        return data

class WeaponName(Enum):
    CANDLESTICK = "Candlestick"
    DAGGER = "Dagger"
    LEAD_PIPE = "Lead Pipe"
    REVOLVER = "Revolver"
    ROPE = "Rope"
    WRENCH = "Wrench"