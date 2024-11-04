#!/usr/bin/env python3

"""
Move Module

This module contains the Move class:
- Move: Handles the logic for moving a player between rooms

Author: Stephen "Christian" Kocsis
Date: 2024-10-19
"""

class Move:
    """Handles the logic for moving a player."""

    def __init__(self, player, start_location, end_location):
        self.player = player  # The player making the move
        self.start_location = start_location  # Starting room
        self.end_location = end_location  # Ending room

    def validate_move(self):
        """Validate if the move is allowed."""
        if self.start_location is None:
            raise ValueError(f"{self.player.name} is not in any room.")
        
        if self.end_location not in self.start_location.connections:
            raise ValueError(f"Invalid move: {self.player.name} cannot move from {self.start_location.name} to {self.end_location.name}.")

        return True  # Placeholder for actual validation logic

    def execute_move(self):
        """Execute the move and update player position."""
        try:
            if self.validate_move():
                # Update the player's location
                self.player.set_location(self.end_location)
                print(f"{self.player.name} moved from {self.start_location.name} to {self.end_location.name}.")
                # Log the move for player history
                self.log_move()
        except ValueError as e:
            print(e)

    def log_move(self):
        """Log the movement for tracking player actions."""
        # This can/will be expanded to save move history in player statistics or game state
        print(f"Move logged: {self.player.name} moved to {self.end_location.name}.")
        
