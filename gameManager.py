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
from playerTurnManager import TurnPhase
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
        self.num_ready = 0
        self.winner = None
        self.game_start = False
        self.prevent_join = False


        self.new_game(players)

    def parse_message(self, message):
        message = json.loads(message)
        message_type = message["message_type"]
        player_name = message["player_name"]
        match message_type:
            case "player_join":
                if self.prevent_join:
                    return

                # Minimal Version
                if len(self.players) == 0:
                    self.add_player(player_name, "Miss Scarlett")
                elif len(self.players) == 1:
                    self.add_player(player_name, "Colonel Mustard")
                elif len(self.players) == 2:
                    self.add_player(player_name, "Professor Plum")
                elif len(self.players) == 3:
                    self.add_player(player_name, "Mrs. Peacock")
                elif len(self.players) == 4:
                    self.add_player(player_name, "Reverend Green")
                elif len(self.players) == 5:
                    self.add_player(player_name, "Mrs. White")
                else:
                    self.websocket.send("TOO MANY PLAYERS GET OUT")

            case "player_ready":
                self.num_ready += 1
                if self.num_ready == len(self.players) and 3 <= self.num_ready <= 6:
                    self.setup_game()
                    self.prevent_join = True

            case "player_unready":
                self.num_ready -= 1

            # Player move
            case "player_move":
                x = message["x_coord"]
                y = message["y_coord"]
                was_moved = message["was_moved"]
                self.move_player(player_name, x, y, was_moved)

            # Accuse other player
            case "skip_to_accuse":
                self.skip_to_accuse()

            case "skip_to_end":
                self.skip_to_end()

            # Make a claim
            case "make_claim":
                is_accused = message["is_accused"]
                character = message["character"]
                weapon = message["weapon"]
                room = message["room"]
                self.make_claim(is_accused, player_name, character, weapon, room)

            case "next_phase":
                self.next_phase()

            case "set_inactive":
                self.set_current_inactive()

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
        self.winner = None
        for name in WeaponName:
            weapon = Weapon(name)
            self.weapons.append(weapon)
        self.claims_log = ClaimsLog()

        print(players)
        if len(self.players) > 0:
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

    def move_player(self, name, x, y, was_moved):
        player = self.get_player(name)
        player.set_position(x, y)
        player.set_was_moved(was_moved)

    def skip_to_suggest(self):
        self.players[self.index].skip_to_suggest()


    def skip_to_accuse(self):
        self.players[self.index].get_turn_manager().skip_to_accuse()

    def next_phase(self):
        self.players[self.index].get_turn_manager().next_phase()

        if self.players[self.index].get_turn_manager().phase == TurnPhase.END:
            self._advance_to_next_player()

    def skip_to_end(self):
        self.players[self.index].get_turn_manager().skip_to_end()
        self._advance_to_next_player()

    def _advance_to_next_player(self):
        while True:
            self._next_player()

            player = self.players[self.index]
            if player.is_active:
                player.get_turn_manager().start_turn()
                break

    def _next_player(self):
        self.index = (self.index + 1) % len(self.players)

    def set_current_inactive(self):
        self.players[self.index].is_active = False
        self._next_player()

    def make_claim(self, is_accuse, name, character, weapon, room):
        player = self.get_player(name)
        if is_accuse:
            claim = Accusation(player, ClueCharacter(character), WeaponName(weapon), Room(room))
            subject = None
            disprover_name = None

            if self._validate_accusation(claim):
                self.winner = self.get_player(name)
                print(name, " wins!")
            else:
                player.eliminate()
                player.is_active = False
        else:
            claim = Suggestion(player, ClueCharacter(character), WeaponName(weapon), Room(room))
            validation = self._validate_suggestion(claim)
            subject = validation[1]
            disprover_name = validation[2]

        self.claims_log.add_claim(claim, subject, disprover_name)

    def _validate_suggestion(self, claim):
        for i in range(len(self.players)):
            loop_index = (i + 1) % len(self.players)
            player = self.players[loop_index]

            for card in player.get_cards():
                if card.get_subject() in claim.get_subjects():
                    return False, card.get_subject(), player.name

        return True, None, None

    def _validate_accusation(self, claim):
        subjects = claim.get_subjects()
        return (subjects[0].value == self.murder[0].value and subjects[1].value == self.murder[1].value
                and subjects[2].value == self.murder[2].value)

    def reset(self, players=None):
        self.new_game(players)

    # end

    def draw(self):
        return self.deck.pop()

    def set_websocket(self, websocket):
        self.websocket = websocket

    def json_serialize(self):
        print(self.game_start)
        data = {
            "players": [player.dict() for player in self.players],
            "claims": self.claims_log.array_of_claims_dicts(),
            "player_turn": self.players[self.index].name if len(self.players) > 2 else None,
            "winner": None if self.winner is None else self.winner.name,
            "game_start": "game_started" if self.game_start == True else None

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
        print(self.murder)
        print("murder cards in deck:", [c.get_subject().value for c in self.deck if c.get_subject() in [character, room, weapon]])
        print("num cards in deck", len(self.deck))

    async def send_gamestate_to_client(self):
        await self.websocket.send(self.json_serialize())

    # New methods for saving and loading game state
    def save_game_state(self, filename="game_state.json"):
        pass

    def load_game_state(self, filename="game_state.json"):
        pass

    def setup_game(self):
        """Set up the game components."""

        self.game_start = True

        # Randomly select murderer, weapon, and room for the crime
        rand_char = random.choice([c for c in ClueCharacter])
        rand_weapon = random.choice([w for w in WeaponName])
        rand_room = random.choice([r for r in Room])

        self.deck = [c for c in self.deck if c.get_subject() not in [rand_char, rand_weapon, rand_room]]

        self.set_murder(rand_char, rand_weapon, rand_room)

        self.deal_cards()  # Deal cards to players after setup

    def deal_cards(self):
        i = 0
        while len(self.deck) > 0:
            self.players[i].add_cards([self.draw()])
            i = (i + 1) % len(self.players)
