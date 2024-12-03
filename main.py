import asyncio
import json
import time
from websockets.asyncio.server import serve, broadcast

from gameManager import GameManager
from player import ClueCharacter
from room import Room
from weapon import WeaponName

game_manager = GameManager()
connected_clients = []


# this will recieve a message and print to the console
async def handler(websocket):
    game_manager.set_websocket(websocket)
    connected_clients.append(websocket)
    await websocket.send(json.dumps("Hello from server!"))
    await game_manager.send_gamestate_to_client()
    async for message in websocket:
        # handle message appropriately and update game state
        print(message)
        game_manager.parse_message(message)
        #await game_manager.send_gamestate_to_client()
        broadcast(connected_clients,game_manager.json_serialize())


# start server to run forever
async def main():
    async with serve(handler, "", 3000):

        print(game_manager.json_serialize())
        # [print(player.characterHandler.character.value) for player in game_manager.players]
        await asyncio.get_running_loop().create_future()


if __name__ == "__main__":
    print("Starting clue-less server!")

    # instantiate game

    asyncio.run(main())