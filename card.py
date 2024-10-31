#!/usr/bin/env python3

"""
Card Module

This module contains the Card class and its subclasses:
- CharacterCard: Represents a character in the game
- Weapon: Represents a weapon in the game
- Room: Represents a room in the game

Author: Stephen "Christian" Kocsis
Date: 2024-10-30
"""

class Card:
    """Base class for all card types in the game"""
    
    def __init__(self, name, description=""):
        self.name = name # Name of the card
        self.description = description # Brief description of the card

    def get_info(self):
        """Return card information."""
        return f"{self.name}: {self.description}"
    
class CharacterCard(Card):
    """Represents a character card"""
        
    def __init__(self, name, default_location=None, description=""):
        super().__init__(name, description)
        self.default_location = default_location  # The character's default location

    def set_location(self, new_location):
        """Set a new default location for the character"""
        self.default_location = new_location

    def get_info(self):
        """Return character info, including location."""
        return (
            f"{self.name} is in "
            f"{self.default_location if self.default_location else 'unknown location'}."
        )

class Weapon(Card):
    """Represents a weapon card"""

    def __init__(self, name, description="", damage_value=0):
        super().__init__(name, description)
        self.damage_value = damage_value  # Example attribute for weapon damage

    def set_damage(self, damage_value):
        """Set the weapon's damage value."""
        self.damage_value = damage_value

    def get_info(self):
        """Return weapon info, including damage value."""
        return f"{self.name}: {self.description}. Damage: {self.damage_value}"

class Room(Card):
    """Represents a room card"""
    
    def __init__(self, name, description=""):
        super().__init__(name, description)
        self.connections = []  # Rooms connected to this room

    def connect_room(self, room):
        """Connect this room to another room."""
        if room not in self.connections:
            self.connections.append(room)

    def get_connected_rooms(self):
        """Return the names of connected rooms."""
        return [room.name for room in self.connections]

    def get_info(self):
        """Return room info, including connections."""
        connected_names = ', '.join(self.get_connected_rooms())
        return f"{self.name}: {self.description}. Connected rooms: {connected_names if connected_names else 'None'}"
        
