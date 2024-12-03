#!/usr/bin/env python3

"""
Player Turn Looping Logic

Author: Stephen "Christian" Kocsis
Date: 2024-12-2
"""

import asyncio
import websockets
import json
from datetime import datetime
import time
from playerTurnManager import PlayerTurnManager, TurnPhase


class PlayerTurnManagerWithPhase:
    """Manages player turns during the game and communicates with the client via WebSockets."""

    def __init__(self, websocket):
        self.players = []  # List to store dynamically added players
        self.current_turn = 0  # Start with the first player
        self.websocket = websocket  # WebSocket connection for client-server communication
        self.phase = TurnPhase.START  # Start phase is the initial phase

    def add_player(self, player_name):
        """Add a new player to the game."""
        player = Player(player_name)
        self.players.append(player)

    def next_turn(self):
        """Advance to the next player's turn."""
        self.current_turn = (self.current_turn + 1) % len(self.players)

    def get_current_player(self):
        """Return the current player."""
        return self.players[self.current_turn]

    async def handle_turn(self):
        """Handles the logic for each player's turn and sends updates to the client via WebSocket."""
        current_player = self.get_current_player()

        # Send current player turn information to the client
        await self.send_message({
            "type": "turn",
            "player": current_player.name,
            "phase": self.phase.name,  # Send the current phase
            "action_prompt": self.get_action_prompt()  # Get action prompt based on current phase
        })

        action = await self.receive_message()

        # Handle the action based on the current phase
        if self.phase == TurnPhase.START:
            self.phase = TurnPhase.MOVE
        elif self.phase == TurnPhase.MOVE:
            await self.handle_move(action)
        elif self.phase == TurnPhase.SUGGEST:
            await self.handle_suggestion(action)
        elif self.phase == TurnPhase.ACCUSE:
            await self.handle_accusation(action)
        elif self.phase == TurnPhase.REFUTE:
            await self.handle_refutation(action)

        # After handling the action, move to the next phase
        self.next_phase()

    def get_action_prompt(self):
        """Return the appropriate prompt based on the current phase."""
        if self.phase == TurnPhase.START:
            return "Start of Turn"
        elif self.phase == TurnPhase.MOVE:
            return "Choose a move action."
        elif self.phase == TurnPhase.SUGGEST:
            return "Choose a suggestion action."
        elif self.phase == TurnPhase.REFUTE:
            return "Choose a refutation action."
        elif self.phase == TurnPhase.ACCUSE:
            return "Choose an accusation action."

    async def handle_move(self, action):
        """Handle player's move action."""
        await self.send_message({"type": "move", "action": action})

    async def handle_suggestion(self, action):
        """Handle player's suggestion action."""
        await self.send_message({"type": "suggestion", "action": action})

    async def handle_accusation(self, action):
        """Handle player's accusation action."""
        await self.send_message({"type": "accusation", "action": action})

    async def handle_refutation(self, action):
        """Handle player's refutation action."""
        await self.send_message({"type": "refutation", "action": action})

    async def send_message(self, data):
        """Send a message to the client via WebSocket."""
        await self.websocket.send(json.dumps(data))

    async def receive_message(self, prompt=None):
        """Receive a message from the client via WebSocket."""
        if prompt:
            await self.send_message({"type": "prompt", "message": prompt})
        message = await self.websocket.recv()
        return message.strip()

    async def start_turns(self):
        """Start the game and loop through player turns until game over condition is met."""
        game_over = False
        while not game_over:
            await self.handle_turn()  # Handle each player's turn

            time.sleep(1)
            self.next_turn()  # Move to the next player's turn
            game_over = self.check_game_over()  # Check if the game has ended

    def next_phase(self):
        """Advance to the next phase of the turn."""
        self.phase = TurnPhase(self.phase.value + 1)  # Move to next phase

    def check_game_over(self):
        """Placeholder method to check if the game is over."""
        return False  # Modify this to return True when the game should end


class Player:
    """Represents a player in the game."""
    def __init__(self, name):
        self.name = name


async def handler(websocket, path):
    """Handles a WebSocket connection for player turns."""
    turn_manager = PlayerTurnManagerWithPhase(websocket)

    # Wait for players to join dynamically
    while len(turn_manager.players) < 3: 
        await turn_manager.send_message({
            "type": "prompt",
            "message": "Enter your player name:"
        })

        player_name = await turn_manager.receive_message()
        turn_manager.add_player(player_name)
        print(f"{player_name} has joined the game!")

    # Once enough players have joined, start the game loop
    await turn_manager.start_turns()


# Start the WebSocket server
start_server = websockets.serve(handler, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
