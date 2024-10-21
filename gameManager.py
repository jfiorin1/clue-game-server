#!/usr/bin/env python3
"""
GameManager Module

This module contains the GameManager class and its associated functions:

Author: Nick Weiner
Date: 2024-10-20
"""
import json
from enum import Enum
import claimsLog
from player import Player
from playerTurnManager import PlayerTurnManager

class GameState(Enum):
    GameStart = 1
    CharacterSelection = 2
    DealCards = 3
    GameBoard = 4
    PlayerTurn = 5
    PlayerWin = 6
    PlayerLoss = 7
    GameOver = 8

class GameManager:

    def __init__(self, players, weapons, claimsLog, gameState):
        self.players = players
        self.index = 0
        self.weapons = weapons
        self.claimsLog = claimsLog
        self.gameState = gameState

    def json_serialize(self):
        data = {
            "players": [player.json_serialize() for player in self.players],
            "weapons": [weapon.json_serialize() for weapon in self.weapons],
            "claims": claimsLog.json_serialize()
        }

        return json.dumps(data)

    def next_phase(self):
        self.players[self.index].turn.next_phase()

    def next_player(self):
        index = (self.index + 1) % len(self.players)
        self.players[index].turn.start_turn()

    def game_state(self):
        if self.gameState == GameState.GameStart:
            print("In game start state")
            # Character selection screen
            # First client to join is defined as the "host"
            # Host is given the option to start the game once at least three players have joined

            # CLI message: "Welcome to Clue", "You are the host", "Write 'start' to start game"
            # GUI image: Home screen, start button

            #Next state = GameStart

            # Trigger to next state: if there are 3 or more players, and the host has prompted game start


            pass
        elif self.gameState == GameState.CharacterSelection:
            print("In character selection state")
            # Character selection screen
            # Prompt players to pick there characters, one player at a time

            # CLI message: "Welcome to Clue", "You are the host", "Write 'start' to start game"
            # GUI image: Home screen, start button

            #Next state: DealCards
            self.gameState = 3

            # Trigger to next state: Host presses "start button" on start screen
            pass
        elif self.gameState == GameState.DealCards:
            print("In Deal cards state")
            #Deal cards screen

            #randomly choose the "secret envelope" which is the combination of room, character, and weapon that everyone will try to guess
            #randomly deal cards to players, these include CharacterCard, RoomCard, and WeaponCard

            # CLI message:  "Your cards are x,y,z", "Host write continue to proceed"
            # GUI image: Home screen, start button

            #Next state: GameBoard
            self.gameState = 4

            #Trigger to next state: Host presses "continue" button (GUI) Host types "continue"

            pass
        elif self.gameState == GameState.GameBoard:
            print("In game board state")
            #Game board screen

            # Shows the game board, initialized with the layout outlined in the requirements
            # Updates the game board after player movements, accusations, and suggestions

            # CLI message:  ASCII art of game board
            # GUI image: Game board showing location of all characters and weapons, any animations of player moves (dream feature)

            # Next state: PlayerTurn
            self.gameState = 5

            # Trigger to next state: time

            pass
        elif self.gameState == GameState.PlayerTurn:
            print("In Player Turn Screen")
            # Player Turn Screen

            # Utilizes playerTurnManager to carry out the logic for moves, accusations, suggestions
            # Gives the UI the messages to activate proper rendering for player turns

            # CLI message:  "Player x turn"
            # GUI image: Game board showing location of all characters and weapons, any animations of player moves (dream feature)

            #Next state: GameBoard, PlayerWin, PlayerLoss
            if 1:
                self.gameState = 6
            elif 1:
                self.gameState = 7
            elif 1:
                self.gameState = 4

            # Trigger to next state: time

            pass

        elif self.gameState == GameState.PlayerWin:
            print("In Player Win Screen")
            # Player Win Screen

            # Shows all actors the guess that the player made
            # Says to all actors it was correct

            # CLI message:  "Player x had the correct guess of RoomCard, Character Card, WeaponCard"
            # GUI image: Card selection, correct combination

            # Next state: GameOver

            # Trigger to next state: time
            pass
        elif self.gameState == GameState.PlayerLoss:
            print("In Player Loss Screen")
            # Player Loss Screen

            # Shows all actors the guess that the player made
            # Says to all actors it was false

            # CLI message:  "Player x had an incorrect guess of RoomCard, Character Card, WeaponCard"
            #               "Player x is now eliminated"
            # GUI image: Card selection, incorrect combination

            # Next state: GameBoard
            self.gameState =  4

            # Trigger to next state: time
            pass
        elif self.gameState == GameState.GameOver:
            print("In Game Over Screen")

            # CLI message:  "Game is over, thanks for playing"
            # GUI image: Game over screen

            # Next state: GameStart
            self.gameState = 1

            # Trigger to next state: host presses game restart
            pass

        else:
            print("ERROR: unkown game state")



gameManager = GameManager()