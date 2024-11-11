#!/usr/bin/env python3

"""
Game Module

This module contains the Game class:
- Game: Manages the overall game logic, player interactions, and game flow.

Author: Stephen "Christian" Kocsis
Date: 2024-10-30
"""

import pygame
import random
from main import game_manager
from gameManager import GameManager
from player import Player, ClueCharacter
from room import Room
from weapon import WeaponName


class GameInstance:
    """Manages the overall logic of the Clue game."""
    
    def __init__(self):
        self.gameManager = GameManager()

        # Initialize Pygame
        # This needs to be improved for working GUI - is a placeholder
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('Clue Game')
        self.font = pygame.font.Font(None, 36)

        # { ClueCharacter: Player | None }
        self.player_dict = {}

    def add_player(self, name, character):
        player = Player(name, character)
        self.gameManager.add_player(player)

    def setup_game(self):
        """Set up the game components."""

        # Randomly select murderer, weapon, and room for the crime
        rand_char = random.choice([c for c in ClueCharacter])
        rand_weapon = random.choice([w for w in WeaponName])
        rand_room = random.choice([r for r in Room])

        self.gameManager.set_murder(rand_char, rand_weapon, rand_room)

        self.deal_cards()  # Deal cards to players after setup

    def deal_cards(self):
        """Distribute cards among players."""
        for player in self.gameManager.players:
            cards = []
            for i in range(3):
                cards.append(game_manager.draw())
            player.add_cards(cards)

    def view_history(self):
        """Display the history of suggestions and accusations."""
        print("\nHistory:")
        for claim in self.gameManager.get_claims_log():
            print(claim.make_string())

    def initialize_players(self, num_ai_players=0):
        """Initialize players and their characters, including AI players."""
        for character in self.characters:
            character.set_location(self.rooms[0])  # Start all characters in the first room
            self.players.append(character)  # Add characters as players for simplicity
        
        # Add AI-controlled players
        # for i in range(num_ai_players):
        #     ai_character = ClueCharacter(f"AI Player {i+1}")
        #     ai_character.set_location(self.rooms[0])
        #     self.players.append(ai_character)

    def start_game(self):
        """Logic to start the game."""
        num_ai_players = int(input("Enter the number of AI players (0 for none): "))
        self.initialize_players(num_ai_players)  # Set up players
        self.play_game()           # Begin the game loop

    def play_game(self):
        """Main game loop."""
        while not self.game_over:
            current_player = self.players[self.current_player_index]
            print(f"\nIt's {current_player.name}'s turn.")
            self.handle_turn(current_player)  # Call method to handle the player's turn
            self.save_game()  # Save the game after each turn
            self.next_turn()  # Move to the next player

            # Pygame Event Loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                # Add more event handling for user inputs

            # Rendering Code (to be filled)
            self.screen.fill((255, 255, 255))  # Clear screen with white
            # Draw elements like rooms, characters, and UI
            pygame.display.flip()  # Update the display
        


# Main execution
if __name__ == "__main__":
    clue_game = GameInstance()  # Create a new Game instance
    clue_game.start_game()  # Start the game
