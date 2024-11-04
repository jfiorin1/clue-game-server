#!/usr/bin/env python3

"""
Game Module

This module contains the Game class:
- Game: Manages the overall game logic, player interactions, and game flow.

Author: Stephen "Christian" Kocsis
Date: 2024-10-30
"""

import json
import pygame
import random
from card import Card
from claim import Claim
from character import ClueCharacter
from move import Move

class Game:
    """Manages the overall logic of the Clue game."""
    
    def __init__(self):
        self.players = []           # List of players (both human and AI)
        self.rooms = []             # List of rooms
        self.weapons = []           # List of weapons
        self.characters = []        # List of character cards
        self.current_player_index = 0
        self.game_over = False
        self.murderer = None        # To hold the actual murderer, weapon, and room
        
        self.suggestions_history = []  # Track all suggestions made
        self.accusations_history = []   # Track all accusations made
    
        self.load_game()           # Load the game state from a JSON file
        if not self.players:       # If no players are loaded, setup a new game
            self.setup_game()       # Set up the game components

        # Initialize Pygame
        # This needs to be improved for working GUI - is a placeholder
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('Clue Game')
        self.font = pygame.font.Font(None, 36)

    def setup_game(self):
        """Set up the game components (rooms, weapons, characters)."""
        # Create rooms
        kitchen = Card.Room("Kitchen")
        ballroom = Card.Room("Ballroom")
        conservatory = Card.Room("Conservatory")
        dining_room = Card.Room("Dining Room")
        lounge = Card.Room("Lounge")
        hall = Card.Room("Hall")
        study = Card.Room("Study")
        library = Card.Room("Library")
        billiard_room = Card.Room("Billiard Room")

        # Connect rooms
        kitchen.connect_room(ballroom)
        ballroom.connect_room(conservatory)
        conservatory.connect_room(dining_room)
        dining_room.connect_room(lounge)
        lounge.connect_room(hall)
        hall.connect_room(study)
        study.connect_room(library)
        library.connect_room(billiard_room)
        billiard_room.connect_room(kitchen)

        self.rooms.extend([kitchen, ballroom, conservatory, dining_room, lounge,
                           hall, study, library, billiard_room])  # Add rooms to the game

        # Create weapons
        self.weapons.extend([
            Card.Weapon("Candlestick"),
            Card.Weapon("Dagger"),
            Card.Weapon("Lead Pipe"),
            Card.Weapon("Revolver"),
            Card.Weapon("Rope"),
            Card.Weapon("Wrench")
        ])  # Add weapons to the game

        # Create characters
        self.characters.extend([
            ClueCharacter("Miss Scarlet"),
            ClueCharacter("Colonel Mustard"),
            ClueCharacter("Mrs. White"),
            ClueCharacter("Mr. Green"),
            ClueCharacter("Mrs. Peacock"),
            ClueCharacter("Professor Plum")
        ])  # Add characters to the game.

        # Randomly select murderer, weapon, and room for the crime
        self.murderer = {
            "character": random.choice(self.characters),
            "weapon": random.choice(self.weapons),
            "room": random.choice(self.rooms)
        }

        self.deal_cards()  # Deal cards to players after setup

    def deal_cards(self):
        """Distribute cards among players."""
        all_cards = self.characters + self.weapons + self.rooms
        random.shuffle(all_cards)  # Shuffle all cards

        while all_cards:
            for player in self.players:
                if all_cards:
                    card = all_cards.pop(0)  # Draw the top card
                    player.add_card(card)  # Give card to player

    def load_game(self):
        """Load game state from a JSON file."""
        # This needs to be integrated with the JSON file - is a placeholder
        try:
            with open("game_state.json", "r") as file:
                data = json.load(file)
                self.players = [ClueCharacter(player['name']) for player in data['players']]
                self.rooms = [Card.Room(room['name']) for room in data['rooms']]
                self.weapons = [Card.Weapon(weapon['name']) for weapon in data['weapons']]
                self.murderer = data['murderer']
                for player in self.players:
                    player.default_location = next(room for room in self.rooms if room.name == player['location'])
                self.suggestions_history = data.get("suggestions_history", [])
                self.accusations_history = data.get("accusations_history", [])
                # Load player statistics
                for player_data in data.get("player_stats", []):
                    player = next((p for p in self.players if p.name == player_data['name']), None)
                    if player:
                        player.statistics = player_data['statistics']
        except FileNotFoundError:
            print("No saved game found. Starting a new game.")
        except json.JSONDecodeError:
            print("Error reading the saved game file. Starting a new game.")

    def save_game(self):
        """Save the current game state to a JSON file."""
        game_state = {
            "players": [{"name": player.name, "location": player.default_location.name} for player in self.players],
            "rooms": [{"name": room.name} for room in self.rooms],
            "weapons": [{"name": weapon.name} for weapon in self.weapons],
            "murderer": {
                "character": {"name": self.murderer["character"].name},
                "weapon": {"name": self.murderer["weapon"].name},
                "room": {"name": self.murderer["room"].name}
            },
            "suggestions_history": self.suggestions_history,
            "accusations_history": self.accusations_history,
            "player_stats": [{"name": player.name, "statistics": player.statistics} for player in self.players]
        }
        with open("game_state.json", "w") as file:
            json.dump(game_state, file)
        print("Game state saved.")

    def reset_game(self):
        """Reset the game to its initial state."""
        print("Resetting the game...")
        self.players.clear()
        self.rooms.clear()
        self.weapons.clear()
        self.characters.clear()
        self.suggestions_history.clear()
        self.accusations_history.clear()
        self.setup_game()
        self.current_player_index = 0
        self.game_over = False
        print("Game has been reset.")

    def view_history(self):
        """Display the history of suggestions and accusations."""
        print("\nSuggestions History:")
        for suggestion in self.suggestions_history:
            print(f"- {suggestion}")

        print("\nAccusations History:")
        for accusation in self.accusations_history:
            print(f"- {accusation}")

    def initialize_players(self, num_ai_players=0):
        """Initialize players and their characters, including AI players."""
        for character in self.characters:
            character.set_location(self.rooms[0])  # Start all characters in the first room
            self.players.append(character)  # Add characters as players for simplicity
        
        # Add AI-controlled players
        for i in range(num_ai_players):
            ai_character = ClueCharacter(f"AI Player {i+1}")
            ai_character.set_location(self.rooms[0])
            self.players.append(ai_character)

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

    def handle_turn(self, player):
        """Handle a player's turn, including movement, suggestions, and accusations."""
        if isinstance(player, ClueCharacter) and player.name.startswith("AI Player"):
            self.ai_turn(player)
        else:
            print(f"Current location: {player.get_info()}")
            available_rooms = [room for room in self.rooms if room != player.default_location]
            print("Available rooms to move to:")
            for i, room in enumerate(available_rooms):
                print(f"{i + 1}: {room.name}")

            # Player input for movement
            move_choice = input("Choose a room number to move: ")
            try:
                move_index = int(move_choice) - 1
                if move_index < 0 or move_index >= len(available_rooms):
                    print("Invalid room choice. Please try again.")
                    return
                move = Move(player, player.default_location, available_rooms[move_index])
                move.execute_move()  # Attempt to move to the selected room

                # After moving, allow suggestion or accusation
                action_choice = input("Would you like to make a suggestion (s), an accusation (a), or view history (h)? ").lower()
                if action_choice == 's':
                    self.make_suggestion(player)
                elif action_choice == 'a':
                    self.make_accusation(player)
                elif action_choice == 'h':
                    self.view_history()
                elif action_choice == 'r':
                    self.reset_game()
                else:
                    print("Invalid choice, proceeding to the next player.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def ai_turn(self, player):
        """Handle the turn for an AI player."""
        print(f"{player.name}'s turn (AI).")
        
        # AI decides to move to an adjacent room
        available_rooms = [room for room in self.rooms if room != player.default_location]
        move_choice = random.choice(available_rooms)
        move = Move(player, player.default_location, move_choice)
        move.execute_move()  # Execute the move

        # AI makes a suggestion based on the current room and its known cards
        known_weapons = [w.name for w in player.cards if isinstance(w, Card.Weapon)]
        known_characters = [c.name for c in player.cards if isinstance(c, ClueCharacter)]
        possible_weapons = [w.name for w in self.weapons if w.name not in known_weapons]
        possible_characters = [c.name for c in self.characters if c.name not in known_characters]
        
        # If possible weapons or characters exist, AI makes a suggestion
        if possible_weapons and possible_characters:
            weapon_choice = random.choice(possible_weapons)
            character_choice = random.choice(possible_characters)
            suggestion = Claim.Suggestion(player.name, weapon_choice, character_choice, player.default_location.name)
            print(f"{player.name} suggests: {suggestion}")

            # AI handles the suggestion
            self.handle_suggestion(suggestion)

        # AI may make an accusation based on knowledge
        if (len(known_weapons) + len(known_characters) >= 3) and random.random() < 0.5:  # 50% chance to make an accusation if it has info - can change this
            accusation = Claim.Accusation(player.name, random.choice(possible_weapons), random.choice(possible_characters), player.default_location.name)
            print(f"{player.name} accuses: {accusation}")
            self.accusations_history.append(str(accusation))  # Log the accusation
            if (accusation.weapon == self.murderer["weapon"]["name"] and
                    accusation.character == self.murderer["character"]["name"] and
                    accusation.room == self.murderer["room"]["name"]):
                print(f"{player.name} has won the game!")
                self.game_over = True
            else:
                print(f"{player.name}'s accusation was incorrect.")
        
    def make_suggestion(self, player):
        """Allow the player to make a suggestion."""
        print("Make a suggestion:")
        weapon_choice = input("Choose a weapon: " + ", ".join([w.name for w in self.weapons]) + ": ")
        character_choice = input("Choose a character: " + ", ".join([c.name for c in self.characters]) + ": ")
        room_choice = player.default_location.name  # Suggestion made in the current room

        suggestion = Claim.Suggestion(player.name, weapon_choice, character_choice, room_choice)
        self.suggestions_history.append(str(suggestion))  # Log the suggestion
        print(f"{player.name} suggests: {suggestion}")

        # Logic to handle the suggestion (disprove it)
        self.handle_suggestion(suggestion)

    def handle_suggestion(self, suggestion):
        """Check if any player can disprove the suggestion."""
        can_disprove = False
        disproving_player = None
        disproving_cards = []  # Track which cards can disprove the suggestion
        for player in self.players:
            if player.has_card(suggestion.weapon):
                disproving_cards.append(suggestion.weapon)
            if player.has_card(suggestion.character):
                disproving_cards.append(suggestion.character)
        
        if disproving_cards:
            can_disprove = True
            disproving_player = random.choice(self.players)  # Randomly select a player who can disprove
            print(f"{disproving_player.name} can disprove the suggestion with their card(s).")
            for card in disproving_cards:
                print(f"{disproving_player.name} shows the {card}.")
        else:
            print("No one can disprove the suggestion.")

    def make_accusation(self, player):
        """Allow the player to make an accusation."""
        print("Make an accusation:")
        weapon_choice = input("Choose a weapon: " + ", ".join([w.name for w in self.weapons]) + ": ")
        character_choice = input("Choose a character: " + ", ".join([c.name for c in self.characters]) + ": ")
        room_choice = input("Choose a room: " + ", ".join([r.name for r in self.rooms]) + ": ")

        accusation = Claim.Accusation(player.name, weapon_choice, character_choice, room_choice)
        self.accusations_history.append(str(accusation))  # Log the accusation
        print(f"{player.name} accuses: {accusation}")

        # Check if the accusation is correct
        if (accusation.weapon == self.murderer["weapon"]["name"] and
                accusation.character == self.murderer["character"]["name"] and
                accusation.room == self.murderer["room"]["name"]):
            print(f"{player.name} has won the game!")
            self.game_over = True
        else:
            print(f"{player.name}'s accusation was incorrect.")
            player.statistics['accusations_made'] += 1  # Increment the accusation count

    def next_turn(self):
        """Move to the next player's turn."""
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

# Main execution
if __name__ == "__main__":
    clue_game = Game()  # Create a new Game instance
    clue_game.start_game()  # Start the game
