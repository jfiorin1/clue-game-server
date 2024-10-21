#!/usr/bin/env python3
"""
GameManager Module

This module contains the GameManager class and its associated functions:

Author: Nick Weiner
Date: 2024-10-20
"""
import json

from claimsLog import ClaimsLog
from weapon import WeaponName, Weapon


class GameManager:

    def __init__(self, players=None):
        if players is None:
            players = []
        self.players = players
        self.index = 0
        self.weapons = []
        self.websocket = None

        for name in WeaponName:
            weapon = Weapon(name)
            self.weapons.append(weapon)

        self.claims_log = ClaimsLog()

    def set_websocket(self, websocket):
        self.websocket = websocket

    def json_serialize(self):
        data = {
            "players": [player.dict() for player in self.players],
            "weapons": [weapon.dict() for weapon in self.weapons],
            "claims": self.claims_log.array_of_claims_dicts()
        }

        return json.dumps(data)

    def send_gamestate_to_client(self):
        self.websocket.send(self.json_serialize())

    def next_phase(self):
        self.players[self.index].turn.next_phase()

    def next_player(self):
        index = (self.index + 1) % len(self.players)
        self.players[index].turn.start_turn()