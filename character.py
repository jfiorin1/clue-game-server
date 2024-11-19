#!/usr/bin/env python3

"""
Character Module

This module contains the ClueCharacter class:
- ClueCharacter: Represents a character with a name and location

Author: Stephen "Christian" Kocsis
Date: 2024-10-30
"""

class ClueCharacter:
    """Represents a character in the Clue game"""
    
    def __init__(self, name, default_location=None, description=""):
        self.name = name  # Store the name of the character
        self.default_location = default_location  # Store the default location
        self.cards = []  # Cards held by the character
        self.statistics = {  # Initialize player statistics
            'suggestions_made': 0,
            'successful_suggestions': 0,
            'accusations_made': 0,
            'successful_accusations': 0,
            'failed_suggestions': 0,  # Track failed suggestions
            'failed_accusations': 0  # Track failed accusations
        }
        self.history = []  # History of actions taken by the character

    def add_card(self, card):
        """Add a card to the character's hand."""
        self.cards.append(card)

    def has_card(self, card_name):
        """Check if the character has a specific card."""
        return any(card.name == card_name for card in self.cards)

    def set_location(self, new_location):
        """Set a new location for the character."""
        self.default_location = new_location
        self.history.append(f"{self.name} moved to {new_location.name}")

    def make_suggestion(self, weapon, character):
        """Record a suggestion made by the character."""
        self.statistics['suggestions_made'] += 1
        self.history.append(f"{self.name} suggested: {weapon} and {character}.")
        
        # Assume the suggestion could fail or succeed
        success = self._check_suggestion(weapon, character)
        if success:
            self.statistics['successful_suggestions'] += 1
            return f"{self.name} suggests that {weapon} was used by {character} in {self.default_location.name}."
        else:
            self.statistics['failed_suggestions'] += 1
            return f"{self.name} suggests that {weapon} was used by {character} in {self.default_location.name}, but the suggestion was not valid."

    def make_accusation(self, weapon, character):
        """Record an accusation made by the character."""
        self.statistics['accusations_made'] += 1
        self.history.append(f"{self.name} accused: {weapon} and {character}.")
        
        # Assume the accusation could fail or succeed
        success = self._check_accusation(weapon, character)  # Example of checking accusation validity
        if success:
            self.statistics['successful_accusations'] += 1
            return f"{self.name} accuses that {weapon} was used by {character} in {self.default_location.name}."
        else:
            self.statistics['failed_accusations'] += 1
            return f"{self.name} accuses that {weapon} was used by {character} in {self.default_location.name}, but the accusation was incorrect."

    def _check_suggestion(self, weapon, character):
        """Check if a suggestion is valid."""
        if self.has_card(weapon) or self.has_card(character):
            return False
        return True

    def _check_accusation(self, weapon, character):
        """Check if an accusation is correct."""
        actual_solution = game_state.solution
        if (weapon, character) == actual_solution:
            return True
        return False

    def get_info(self):
        """Return character info, including location and cards."""
        card_names = ', '.join(card.name for card in self.cards) if self.cards else 'No cards'
        return (
            f"{self.name} is in {self.default_location if self.default_location else 'unknown location'}. "
            f"Cards held: {card_names}. "
            f"Statistics - Suggestions Made: {self.statistics['suggestions_made']}, "
            f"Successful Suggestions: {self.statistics['successful_suggestions']}, "
            f"Accusations Made: {self.statistics['accusations_made']}, "
            f"Successful Accusations: {self.statistics['successful_accusations']}, "
            f"Failed Suggestions: {self.statistics['failed_suggestions']}, "
            f"Failed Accusations: {self.statistics['failed_accusations']}."
        )

    def serialize(self):
        """Serialize the character's state for saving."""
        return {
            "name": self.name,
            "default_location": self.default_location.name if self.default_location else None,
            "cards": [card.name for card in self.cards],
            "statistics": self.statistics,
            "history": self.history
        }

    @classmethod
    def deserialize(cls, data):
        """Deserialize character data from JSON."""
        character = cls(data['name'], data.get('default_location'))
        character.statistics = data['statistics']
        character.history = data['history']
        character.cards = [Card.CharacterCard(name) for name in data['cards']]  # Make sure Card is defined
        return character
        
