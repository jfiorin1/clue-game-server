#!/usr/bin/env python3

"""
Claim Module

This module contains the Claim class and its subclasses:
- Suggestion: Represents a suggestion made by a player
- Accusation: Represents an accusation made by a player

Author: Stephen "Christian" Kocsis
Date: 2024-10-19
"""

class Claim:
    """Base class for claims made during the game"""
    class Suggestion:
        """Represents a suggestion made by a player"""
        def __init__(self, weapon, character, room):
            self.weapon = weapon
            self.character = character
            self.room = room
            # Will include validation and processing logic for suggestions

    class Accusation:
        """Represents an accusation made by a player"""
        def __init_(self, weapon, character, room):
            self.weapon = weapon
            self.character = character
            self.room = room
            # Will include validation and processing logic for accusations
