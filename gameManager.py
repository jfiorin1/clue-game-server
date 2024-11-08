#!/usr/bin/env python3
"""
GameManager Module

This module contains the GameManager class and its associated functions:

Author: Nick Weiner
Date: 2024-10-20
"""
import json
import os

from claimsLog import ClaimsLog
from clueMap import ClueMap
from deserializer import Deserializer
from weapon import WeaponName, Weapon
from player import Player, ClueCharacter
from room import Room

class GameManager:

    def __init__(self, players=None):
        if players is None:
            players = []
        self.players = players
        self.index = 0
        self.weapons = []
        self.websocket = None
        self.clue_map = ClueMap()
        self.deserializer = Deserializer(self)

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

    def json_deserialize(self, jsonstirng):
        self.deserializer.deserialize_game(jsonstirng)

    def set_objects(self, players, weapons, claims_log):
        self.players = players
        self.weapons = weapons
        self.claims_log = claims_log
        self.clue_map = ClueMap()

    def get_player(self, name):
        for player in self.players:
            if player.name == name:
                return player

        return None

    async def send_gamestate_to_client(self):
        await self.websocket.send(self.json_serialize())

    def next_phase(self):
        self.players[self.index].turn.next_phase()

    def next_player(self):
        index = (self.index + 1) % len(self.players)
        self.players[index].turn.start_turn()

    # New methods for saving and loading game state
    def save_game_state(self, filename="game_state.json"):
        """Saves the current game state to a JSON file."""
        data = {
            "players": [player.dict() for player in self.players],
            "weapons": [weapon.dict() for weapon in self.weapons],
            "claims": self.claims_log.array_of_claims_dicts(),
            "current_turn": self.index
        }
        with open(filename, 'w') as file:
            json.dump(data, file)
        print(f"Game state saved to {filename}")

    def load_game_state(self, filename="game_state.json"):
        """Loads the game state from a JSON file."""
        if not os.path.exists(filename):
            print(f"No saved game state found at {filename}")
            return

        with open(filename, 'r') as file:
            data = json.load(file)

        # Reconstruct players
        self.players = [Player(**player_data) for player_data in data.get("players", [])]

        # Reconstruct weapons and place them in the correct rooms
        self.weapons = [Weapon(WeaponName[weapon_data["name"]]) for weapon_data in data.get("weapons", [])]
        for weapon, weapon_data in zip(self.weapons, data.get("weapons", [])):
            room_coordinates = weapon_data.get("room")
            if room_coordinates:
                weapon.set_room(Room.get_room(tuple(room_coordinates)))

        # Load the claims log
        self.claims_log = ClaimsLog()
        for claim_data in data.get("claims", []):
            # Assuming claims are stored as dicts and can be re-constructed here
            # Modify as necessary if ClaimsLog has specific add_claim requirements
            self.claims_log.add_claim(claim_data)

        # Restore the current turn index
        self.index = data.get("current_turn", 0)

        print(f"Game state loaded from {filename}")

