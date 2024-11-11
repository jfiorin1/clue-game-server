#!/usr/bin/env python3
"""
PlayerTurnManager Module

This module contains the PlayerTurnManager Class and its associated classes and functions
Author: Nick Weiner
Date: 2024-10-19
"""

from enum import Enum

class PlayerTurnManager:
    def __init__(self):
        self.phase = TurnPhase.START

    def get_current_phase(self):
        return self.phase

    def start_turn(self):
        self.phase = TurnPhase.START

    def next_phase(self):
        self.phase = TurnPhase(self.phase.value + 1)

    def skip_to_accuse(self):
        self.phase = TurnPhase.ACCUSE

class TurnPhase(Enum):
    START = 0
    MOVE = 1
    SUGGEST = 2
    REFUTE = 3
    ACCUSE = 4