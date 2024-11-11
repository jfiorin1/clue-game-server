#!/usr/bin/env python3
"""
GameManager Module

This module contains the GameManager class and its associated functions:

Author: Nick Weiner
Date: 2024-10-20
"""
import json
import os
import random

from card import CharacterCard, WeaponCard, RoomCard
from claimsLog import ClaimsLog
from clueMap import ClueMap
from weapon import WeaponName, Weapon
from player import Player, ClueCharacter
from room import Room
from deserializer import Deserializer


class GameManager:

    def __init__(self, players=None):
        self.players = None
        self.index = 0
        self.weapons = []
        self.websocket = None
        self.clue_map = None
        self.deserializer = None
        self.murder = None
        self.deck = []
        self.claims_log = None

        self.new_game(players)

    def new_game(self, players):
        if players is None:
            players = []
        self.players = players
        self.index = 0
        self.weapons = []
        self.websocket = None
        self.clue_map = ClueMap(self)
        self.deserializer = Deserializer(self)
        self.murder = None
        self.deck = self.get_all_cards()
        for name in WeaponName:
            weapon = Weapon(name)
            self.weapons.append(weapon)
        self.claims_log = ClaimsLog()

        rand_character = random.choice([c for c in ClueCharacter])
        rand_weapon = random.choice([w for w in WeaponName])
        rand_room = random.choice([r for r in Room])

        self.set_murder(rand_character, rand_weapon, rand_room)

    def get_all_cards(self):
        cards = []
        for character in ClueCharacter:
            char_card = CharacterCard(character)
            cards.append(char_card)

        for weapon in WeaponName:
            weapon_card = WeaponCard(weapon)
            cards.append(weapon_card)

        for room in Room:
            room_card = RoomCard(room)
            cards.append(room_card)

        random.shuffle(cards)
        return cards

    def add_player(self, player):
        self.players.append(player)

    def move_player(self, player, x, y):
        pass

    def advance_player_turn(self, player):
        player.get_turn_manager().next_phase()

    def skip_to_accuse(self, player):
        player.get_turn_manager().skip_to_accuse()

    def make_claim(self, is_accuse, player, character, weapon, room):
        pass

    def next_player(self):
        self.index = (self.index + 1) % len(self.players)

    def reset(self, players=None):
        self.new_game(players)

    def draw(self):
        return self.deck.pop()

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

    def get_claims_log(self):
        return self.claims_log.get_log()

    def set_murder(self, character, weapon, room):
        self.murder = (character, weapon, room)

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

    def add_player(self, name, character):
        self.player_dict[name] = character

    def setup_game(self):
        """Set up the game components."""

        # Randomly select murderer, weapon, and room for the crime
        rand_char = random.choice([c for c in ClueCharacter])
        rand_weapon = random.choice([w for w in WeaponName])
        rand_room = random.choice([r for r in Room])

        self.gameManager.set_murder(rand_char, rand_weapon, rand_room)

        self.deal_cards()  # Deal cards to players after setup

    def deal_cards(self):
        """Distribute cards among players."""
        for player in self.gameManager.players:
            cards = []
            for i in range(3):
                cards.append(game_manager.draw())
            player.add_cards(cards)

