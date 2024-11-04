#!/usr/bin/env python3

"""
Move Module

This module contains the Move class:
- Move: Handles the logic for moving a player between rooms

Author: Stephen "Christian" Kocsis
Date: 2024-10-19
"""

class Move:
    """Handles the logic for moving a player"""

    def __init__(self, player, start_location, end_location):
        self.player = player  # The player making the move
        self.start_location = start_location  # Starting room
        self.end_location = end_location  # Ending room

    def validate_move(self):
        """Validate if the move is allowed"""
        # Will include logic to check if the move is legal based on game rules
        return True  # Placeholder for actual validation logic

    def execute_move(self):
        """Execute the move and update player position"""
        self.player.set_location(
            self.end_location)
        # Will involve updating the game state and notifying other players
