#!/usr/bin/env python3
"""
GameManager Module

This module contains the GameManager class and its associated functions:

Author: Nick Weiner & Christopher Pohl
Date: 2024-10-20
"""
import json
import os
import random
from operator import index

from card import CharacterCard, WeaponCard, RoomCard
from claim import Accusation, Suggestion
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

    def parse_message(self, message):
        message_type = message["message_type"]
        player_name = message["player_name"]
        match message_type:
            case "player_join":
                # Minimal Version
                if len(self.players) == 0:
                    self.add_player(player_name, "Colonel Mustard")
                elif len(self.players) == 1:
                    self.add_player(player_name, "Professor Plum")
                elif len(self.players) == 2:
                    self.add_player(player_name, "Miss Scarlett")
                else:
                    self.websocket.send("TOO MANY PLAYERS GET OUT")

            # Player move
            case "player_move":
                x = message["x_coord"]
                y = message["y_coord"]
                self.move_player(player_name, x, y)

            # Accuse other player
            case "skip_to_accuse":
                self.skip_to_accuse(player_name)

            # Make a claim
            case "make_claim":
                is_accused = message["is_accused"]
                character = message["character"]
                weapon = message["weapon"]
                room = message["room"]
                self.make_claim(is_accused, player_name, character, weapon, room)

            case _:
                print("Unknown message type")

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

        self.setup_game()

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

    # client initiated functions

    def add_player(self, name, character):
        player = Player(name, ClueCharacter(character), self)
        self.players.append(player)

    def move_player(self, name, x, y):
        player = self.get_player(name)
        player.set_position(x, y)

    def skip_to_accuse(self, name):
        player = self.get_player(name)
        player.get_turn_manager().skip_to_accuse()

    def make_claim(self, is_accuse, name, character, weapon, room):
        claim = None
        player = self.get_player(name)
        if is_accuse:
            claim = Accusation(player, ClueCharacter(character), WeaponName(weapon), Room(room))
        else:
            claim = Suggestion(player, ClueCharacter(character), WeaponName(weapon), Room(room))

        self.claims_log.add_claim(claim)

    def reset(self, players=None):
        self.new_game(players)

    # end

    def draw(self):
        return self.deck.pop()

    def set_websocket(self, websocket):
        self.websocket = websocket

    def json_serialize(self):
        data = {
            "players": [player.dict() for player in self.players],
            "weapons": [weapon.dict() for weapon in self.weapons],
            "claims": self.claims_log.array_of_claims_dicts(),
            "player_turn": self.players[self.index].name
        }
        return json.dumps(data)

    def json_deserialize(self, jsonstirng):
        self.deserializer.deserialize_game(jsonstirng)

    def set_objects(self, players, weapons, claims_log):
        self.players = players
        self.weapons = weapons
        self.claims_log = claims_log
        self.clue_map = ClueMap(self)

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

    # New methods for saving and loading game state
    def save_game_state(self, filename="game_state.json"):
        pass

    def load_game_state(self, filename="game_state.json"):
        pass

    def setup_game(self):
        """Set up the game components."""

        # Randomly select murderer, weapon, and room for the crime
        rand_char = random.choice([c for c in ClueCharacter])
        rand_weapon = random.choice([w for w in WeaponName])
        rand_room = random.choice([r for r in Room])

        self.deck = [c for c in self.deck if c.get_subject() not in [rand_char, rand_room, rand_room]]

        self.set_murder(rand_char, rand_weapon, rand_room)

        self.deal_cards()  # Deal cards to players after setup

    def deal_cards(self):
        """Distribute cards among players."""
        for player in self.players:
            cards = []
            for i in range(3):
                cards.append(self.draw())
            player.add_cards(cards)
