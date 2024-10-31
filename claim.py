#!/usr/bin/env python3

"""
Claim Module

This module contains the Claim class and its subclasses:
- Suggestion: Represents a suggestion made by a player
- Accusation: Represents an accusation made by a player

Author: Stephen "Christian" Kocsis
Date: 2024-10-30
"""

from datetime import datetime

class Claim:
    """Base class for claims made by players"""
    
    def __init__(self, player_name):
        self.player_name = player_name  # The name of the player making the claim
        self.timestamp = datetime.now()  # The time when the claim was made

    def get_info(self):
        """Return basic information about the claim."""
        return f"Claim by {self.player_name} at {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"


class Suggestion(Claim):
    """Represents a suggestion made by a player"""
    
    def __init__(self, player_name, weapon, character, room):
        super().__init__(player_name)
        self.weapon = weapon
        self.character = character
        self.room = room  # Suggestion made in the current room

    def is_valid(self):
        """Validate the suggestion logic."""
        # Logic to determine if the suggestion is valid
        return True  # Placeholder for actual validation logic

    def get_info(self):
        """Return detailed information about the suggestion."""
        return (
            f"{super().get_info()} - Suggestion: {self.character} used {self.weapon} in {self.room}."
        )


class Accusation(Claim):
    """Represents an accusation made by a player"""
    
    def __init__(self, player_name, weapon, character, room):
        super().__init__(player_name)
        self.weapon = weapon
        self.character = character
        self.room = room  # Accusation made regarding the murder

    def is_valid(self):
        """Validate the accusation logic."""
        # Logic to determine if the accusation is valid
        return True  # Placeholder for actual validation logic

    def get_info(self):
        """Return detailed information about the accusation."""
        return (
            f"{super().get_info()} - Accusation: {self.character} used {self.weapon} in {self.room}."
        )

    def serialize(self):
        """Serialize the accusation to a dictionary."""
        return {
            "player_name": self.player_name,
            "timestamp": self.timestamp.isoformat(),
            "weapon": self.weapon,
            "character": self.character,
            "room": self.room,
            "type": "accusation"
        }

    @classmethod # Class method - bvound to the class and not the instance of the class
    def deserialize(cls, data):
        """Deserialize accusation data from a dictionary."""
        accusation = cls(data['player_name'], data['weapon'], data['character'], data['room'])
        accusation.timestamp = datetime.fromisoformat(data['timestamp'])
        return accusation
        
