#!/usr/bin/env python3
"""
Map Module

This module contains the Map class and its associated functions:

Author: Nick Weiner
Date: 2024-10-20
"""
import random
import json

from room import Room
from gameManager import gameManager

class Map:

    def __init__(self):
        self.room_map = [[None] * 5] * 5
        self.weapon_map = [[None] * 5] * 5
        self.player_map = [[None] * 5] * 5

        for i in range(5):
            for j in range(5):
                self.room_map[i][j] = Room.get_room_by_coordinate((i, j))

        for player in gameManager.players:
            position = player.character.get_default_position()
            self.player_map[position[0]][position[1]] = player

        for weapon in gameManager.weapons:
            weapon.room = random.sample(self.room_map, 1)
            coordinate = weapon.room.get_coordinate()
            self.weapon_map[coordinate[0]][coordinate[1]] = weapon

    def move_weapon(self, weapon, new_room):
        yield NotImplementedError