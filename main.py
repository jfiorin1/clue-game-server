import asyncio
import json
from websockets.asyncio.server import serve

from gameManager import gameManager


# this will recieve a message and print to the console
async def handler(websocket):

    await websocket.send(json.dumps("Hello from server!"))
    # set game state to the start screen
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
