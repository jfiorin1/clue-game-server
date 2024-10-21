#!/usr/bin/env python3
"""
Room Module

This module contains the Room Enum
Author: Nick Weiner
Date: 2024-10-19
"""

from enum import Enum

class Room(Enum):
    STUDY = "Study"
    HALL = "Hall"
    LOUNGE = "Lounge"
    LIBRARY = "Library"
    BILLIARD = "Billiard Room"
    DINING = "Dining Room"
    CONSERVATORY = "Conservatory"
    BALLROOM = "Ballroom"
    KITCHEN = "Kitchen"

    def get_coordinates(self):
        return _room_coordinates[self]

    @staticmethod
    def get_room(coordinates):
        return _reversed_coordinates.get(coordinates, None)

_room_coordinates = {
    Room.STUDY: (0, 0),
    Room.HALL: (2, 0),
    Room.LOUNGE: (4, 0),
    Room.LIBRARY: (0, 2),
    Room.BILLIARD: (2, 2),
    Room.DINING: (4, 2),
    Room.CONSERVATORY: (0, 4),
    Room.BALLROOM: (2, 4),
    Room.KITCHEN: (4, 4)
}

_reversed_coordinates = {v: k for k, v in _room_coordinates.items()}