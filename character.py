#!/usr/bin/env python3

"""
Character Module

This module contains the ClueCharacter class:
- ClueCharacter: Represents a character with a name and location

Author: Stephen "Christian" Kocsis
Date: 2024-10-19
"""

class ClueCharacter:
    """Represents a character in the Clue game"""
    def __init__(self, name, default_location=None):
        self.name = name # Store the name of the character
        self.default_location = default_location # Store the default location
        # Will define how a character moves between rooms

    def set_location(self, new_location):
        """Set a new location for the character"""
        self.default_location = new_location
        # Will involve more complex movement logic

    def get_info(self):
        """Return character info"""
        return (
            f"{self.name} is in "
            f"{self.default_location}."
            if self.default_location
            else "unknown location."
        )
