#!/usr/bin/env python3
"""
Map Module

This module contains the Map class and its associated functions:

Author: Nick Weiner
Date: 2024-10-20
"""

from main import game_manager

class ClueMap:

    def __init__(self):
        self.player_map = [[None] * 5] * 5

        for player in game_manager.players:
            position = player.character.get_default_position()
            self.player_map[position[0]][position[1]] = player

    def get_player_map(self):
        return self.player_map

    def move_player(self, player, position):
        for i in range(0, len(self.player_map)):
            for j in range(0, len(self.player_map[i])):
                if self.player_map[i][j] == player:
                    self.player_map[i][j] = None

        self.player_map[position[0]][position[1]] = player