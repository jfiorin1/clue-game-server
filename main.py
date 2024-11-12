import asyncio
import json
from websockets.asyncio.server import serve

from gameManager import GameManager

game_manager = GameManager()


# this will recieve a message and print to the console
async def handler(websocket):
    game_manager.set_websocket(websocket)
    await websocket.send(json.dumps("Hello from server!"))
    await game_manager.send_gamestate_to_client()
    async for message in websocket:
        # handle message appropriately and update game state
        print(message)
        game_manager.parse_message(message)
        await game_manager.send_gamestate_to_client()


# start server to run forever
async def main():


    async with serve(handler, "", 3000):
        # dummy = {
        #     "message_type": "player_join",
        #     "player_name": "xxXXSniperYoMama420Xxx"
        # }
        # game_manager.parse_message(dummy)
        # game_manager.parse_message(dummy)
        # game_manager.parse_message(dummy)
        # [print(player.characterHandler.character.value) for player in game_manager.players]
        await asyncio.get_running_loop().create_future()


if __name__ == "__main__":
    print("Starting clue-less server!")

    # instantiate game

    asyncio.run(main())
