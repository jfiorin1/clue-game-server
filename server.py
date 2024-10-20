import asyncio
import json
from websockets.asyncio.server import serve

# Load game configuration from JSON file
def load_game_config():
    try:
        with open('game_config.json', 'r') as file:
            game_state = json.load(file)
            print("Game configuration loaded successfully.")
            return game_state
    except FileNotFoundError:
        print("Game configuration file not found.")
        return {}

# Initialize game state
game_state = load_game_config()

# Function to broadcast the current game state to all clients
async def broadcast_game_state(websocket, message=None):
    if message:
        print(f"Received message from client: {message}")
    await websocket.send(json.dumps({"game_state": game_state}))

# WebSocket handler for clients
async def handler(websocket):
    await broadcast_game_state(websocket, "New client connected")
    async for message in websocket:
        print(f"Message received: {message}")
        # Example: Process a move from a client (you could expand this logic)
        game_state['characters'][0]['location'] = "Ballroom"
        await broadcast_game_state(websocket, message)

# Start WebSocket server
async def main():
    async with serve(handler, "", 3000):
        await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
    print("Starting Clue-Less server!")
    asyncio.run(main())
