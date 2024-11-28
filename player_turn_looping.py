import asyncio
import websockets
import json
from datetime import datetime
import time

class PlayerTurnManager:
    """Manages player turns during the game and communicates with the client via WebSockets."""

    def __init__(self, players, websocket):
        self.players = players  # List of all players in the game
        self.current_turn = 0  # Start with the first player
        self.websocket = websocket  # WebSocket connection for client-server communication

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
            "action_prompt": "Choose an action: 1. Suggestion 2. Accusation 3. End Turn"
        })

        action = await self.receive_message()

        if action == '1':  # Suggestion
            character = await self.receive_message("Choose character: ")
            weapon = await self.receive_message("Choose weapon: ")
            room = await self.receive_message("Choose room: ")

            suggestion = Suggestion(current_player, character, weapon, room)
            await self.send_message({
                "type": "suggestion",
                "message": suggestion.make_string()
            })

        elif action == '2':  # Accusation
            character = await self.receive_message("Choose character for accusation: ")
            weapon = await self.receive_message("Choose weapon for accusation: ")
            room = await self.receive_message("Choose room for accusation: ")

            accusation = Accusation(current_player, character, weapon, room)
            await self.send_message({
                "type": "accusation",
                "message": accusation.make_string()
            })

        elif action == '3':  # End Turn
            await self.send_message({
                "type": "turn_end",
                "message": f"{current_player.name}'s turn has ended."
            })

        else:
            await self.send_message({
                "type": "error",
                "message": "Invalid action. Please choose a valid action."
            })
            await self.handle_turn()  # Recursively call the function if the input is invalid

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

    def check_game_over(self):
        """Placeholder method to check if the game is over."""
        return False  # Modify this to return True when the game should end


async def handler(websocket, path):
    # Create a PlayerTurnManager and start the game
    players = [Player("Alice"), Player("Bob"), Player("Charlie")]  # Example list of players
    turn_manager = PlayerTurnManager(players, websocket)
    await turn_manager.start_turns()


# Start the WebSocket server
start_server = websockets.serve(handler, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
