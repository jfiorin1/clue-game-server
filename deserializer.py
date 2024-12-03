#!/usr/bin/env python3
"""
GameManager Module

This module contains the GameManager class and its associated functions:

Author: Nick Weiner
Date: 2024-11-8
"""
import json

from card import CharacterCard, WeaponCard, RoomCard
from claim import Accusation, Suggestion
from claimsLog import ClaimsLog
from weapon import WeaponName, Weapon
from player import Player, ClueCharacter
from room import Room

class Deserializer():
    def __init__(self, gameManager):
        self.gameManager = gameManager

    def deserialize_game(self, jsonString):
        data = json.loads(jsonString)

        players = self.deserialize_players(data)
        weapons = self.deserialize_weapons(data)
        claims_log = self.deserialize_claims(data)

        self.gameManager.set_objects(players, weapons, claims_log)

    def deserialize_claims(self, data):
        claims_log = ClaimsLog()
        for claim in data['claims']:
            suggestion = claim.key == "suggestion"
            body = claim.value

            player = self.gameManager.get_player(body["player"])
            character = ClueCharacter(body["character"])
            weaponName = WeaponName(body["weapon"])
            room = Room(body["room"])

            subject = body['disproving_subject']
            disprover = body['disprover']

            if suggestion:
                claims_log.add_claim(Suggestion(player, character, weaponName, room), subject, disprover)
            else:
                claims_log.add_claim(Accusation(player, character, weaponName, room))

        return claims_log

    def deserialize_weapons(self, data):
        weapons = []
        for weapon in data['weapons']:
            name = WeaponName(weapon["name"])
            room = Room(weapon["room"])
            w = Weapon(name, room)
            weapons.append(w)
        return weapons

    def deserialize_players(self, data):
        players = []
        for player in data['players']:
            p = Player(player["name"], ClueCharacter(player["character"]), self.gameManager)
            p.set_position(player["position"]["x"], player["position"]["y"])

            cards = self.deserialize_cards(player)

            p.add_cards(cards)
            players.append(p)
        return players

    def deserialize_cards(self, player_dict):
        cards = []
        for card in player_dict["cards"]:
            if "character_card" in card:
                character = ClueCharacter(card["character_card"])
                cards.append(CharacterCard(character))
            elif "weapon_card" in card:
                weaponName = WeaponName(card["weapon_card"])
                cards.append(WeaponCard(weaponName))
            elif "room_card" in card:
                room = Room(card["room_card"])
                cards.append(RoomCard(room))
        return cards
