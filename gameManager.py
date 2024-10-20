#!/usr/bin/env python3
"""
GameManager Module

This module contains the GameManager class and its associated functions:

Author: Nick Weiner
Date: 2024-10-20
"""
import json
from player import Player
from playerTurnManager import PlayerTurnManager

class GameManager:

    def __init__(self, players, rooms, weapons, map):
        self.players = players
        self.index = 0
        self.weapons = weapons
        self.map = map

    def json_serialize(self):
        data = {
            "players": [player.json_serialize() for player in self.players],
            "weapons": [weapon.json_serialize() for weapon in self.weapons],
        }

        return json.dumps(data)

    def next_phase(self):
        self.players[self.index].turn.next_phase()

    def next_player(self):
        index = (self.index + 1) % len(self.players)
        self.players[index].turn.start_turn()

gameManager = GameManager()