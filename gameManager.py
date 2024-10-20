#!/usr/bin/env python3
"""
GameManager Module

This module contains the GameManager class and its associated functions:

Author: Nick Weiner
Date: 2024-10-20
"""
import json


class GameManager:

    def __init__(self, players, rooms, weapons, map):
        self.players = players
        self.weapons = weapons
        self.map = map

    def json_serialize(self):
        data = {
            "players": [player.json_serialize() for player in self.players],
            "weapons": [weapon.json_serialize() for weapon in self.weapons],
        }