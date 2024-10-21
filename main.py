import asyncio
import json
from websockets.asyncio.server import serve

from gameManager import GameManager

game_manager = GameManager()

# this will recieve a message and print to the console
async def handler(websocket):
    game_manager.set_websocket(websocket)
    await websocket.send(json.dumps("Hello from server!"))
    async for message in websocket:
        # handle message appropriately and update game state
        print(message)
        # send back a dummy message
        await websocket.send("Message receieved and updated game state")


# start server to run forever
async def main():
    async with serve(handler, "", 3000):
        await asyncio.get_running_loop().create_future()


if __name__ == "__main__":
    print("Starting clue-less server!")

    # instantiate game

    asyncio.run(main())
