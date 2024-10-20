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
        self.phase = TurnPhase.ROLL

    def start_turn(self):
        raise NotImplementedError()

    def next_phase(self):
        raise NotImplementedError()

    def skip_to_accuse(self):
        self.phase = TurnPhase.ACCUSE
        raise NotImplementedError()

class TurnPhase(Enum):
    ROLL = 0
    MOVE = 1
    SUGGEST = 2
    REFUTE = 3
    ACCUSE = 4