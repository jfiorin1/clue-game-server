#!/usr/bin/env python3

"""
PlayerTurnManager Module

This module contains the PlayerTurnManager Class and its associated classes and functions

Author: Christian Kocsis
Date: 2024-12-2
"""

from enum import Enum


class PlayerTurnManager:
    """Manages the phases of each player's turn in the game."""

    def __init__(self):
        self.phase = TurnPhase.START
        self.players = [] 
        self.current_player_index = 0

    def add_player(self, player):
        """Add a player to the game."""
        self.players.append(player)

    def get_current_phase(self):
        """Return the current phase of the game."""
        return self.phase

    def get_current_player(self):
        """Return the current player."""
        return self.players[self.current_player_index]

    def start_turn(self):
        """Start the turn for the first player."""
        self.phase = TurnPhase.MOVE 

    def next_turn(self):
        """Advance to the next player's turn."""
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        self.phase = TurnPhase.MOVE 

    def next_phase(self):
        """Advance to the next phase within the player's turn."""
        if self.phase == TurnPhase.MOVE:
            self.phase = TurnPhase.SUGGEST
        elif self.phase == TurnPhase.SUGGEST:
            self.phase = TurnPhase.ACCUSE
        elif self.phase == TurnPhase.ACCUSE:
            self.phase = TurnPhase.REFUTE
        elif self.phase == TurnPhase.REFUTE:
            self.phase = TurnPhase.MOVE  

    def skip_to_accuse(self):
        """Skip directly to the accusation phase."""
        self.phase = TurnPhase.ACCUSE

class TurnPhase(Enum):
    """Enumerates all possible phases of the player's turn."""
    START = 0
    MOVE = 1
    SUGGEST = 2
    REFUTE = 3
    ACCUSE = 4

class Player:
    """Represents a player in the game."""
    
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name
