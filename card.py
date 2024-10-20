#!/usr/bin/env python3

"""
Card Module

This module contains the Card class and its subclasses:
- CharacterCard: Represents a character in the game
- Weapon: Represents a weapon in the game
- Room: Represents a room in the game

Author: Stephen "Christian" Kocsis
Date: 2024-10-19
"""

class Card:
    """Base class for all card types in the game"""
    class CharacterCard:
        """Represents a character card"""
        def __init__(self, name):
            self.name = name
            set.default_location = None
            # Will define the character's default location

    class Weapon:
        """Represents a weapon card"""
        def __init__(self, name):
            self.name = name
            # Will implement more attributes related to the weapon

    class Room:
        """Represents a room card"""
        def __init__(self, name):
            self.name = name
            # Will implement more attributes related to the room
