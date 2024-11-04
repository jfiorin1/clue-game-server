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

class ClueMap:

    def __init__(self):
        self.weapon_map = {}
        self.player_map = [[None] * 5] * 5

        for player in gameManager.players:
            position = player.character.get_default_position()
            self.player_map[position[0]][position[1]] = player

        for weapon in gameManager.weapons:
            rooms = [room for room in Room]
            weapon.room = rooms[random.randint(0, len(Room) - 1)]
            self.weapon_map[weapon] = weapon.room

    def get_weapons_map(self):
        return self.weapon_map

    def get_player_map(self):
        return self.player_map

    def move_weapon(self, weapon, new_room):
        self.weapon_map[weapon] = new_room
        weapon.room = new_room

    def move_player(self, player, position):
        for i in range(0, len(self.player_map)):
            for j in range(0, len(self.player_map[i])):
                if self.player_map[i][j] == player:
                    self.player_map[i][j] = None

        self.player_map[position[0]][position[1]] = player