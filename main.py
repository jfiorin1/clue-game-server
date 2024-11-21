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
        dummy = {
            "message_type": "player_join",
            "player_name": "xxXXSniperYoMama420Xxx"
        }
        dummy_json = json.dumps(dummy)
        game_manager.parse_message(dummy_json)
        dummy = {
            "message_type": "player_join",
            "player_name": "1xxXXSniperYoMama420Xxx"
        }
        dummy_json = json.dumps(dummy)
        game_manager.parse_message(dummy_json)
        dummy = {
            "message_type": "player_join",
            "player_name": "2xxXXSniperYoMama420Xxx"
        }
        dummy_json = json.dumps(dummy)
        game_manager.parse_message(dummy_json)

        dummy = {
            "message_type": "player_ready",
            "player_name": "xxXXSniperYoMama420Xxx"
        }
        dummy_json = json.dumps(dummy)
        game_manager.parse_message(dummy_json)
        dummy = {
            "message_type": "player_ready",
            "player_name": "1xxXXSniperYoMama420Xxx"
        }
        dummy_json = json.dumps(dummy)
        game_manager.parse_message(dummy_json)
        dummy = {
            "message_type": "player_ready",
            "player_name": "2xxXXSniperYoMama420Xxx"
        }
        dummy_json = json.dumps(dummy)
        game_manager.parse_message(dummy_json)

        dummy = {
            "message_type": "make_claim",
            "player_name": "xxXXSniperYoMama420Xxx",
            "is_accused": True,
            "character": ClueCharacter.MRS_WHITE.value,
            "weapon": WeaponName.ROPE.value,
            "room": Room.HALL.value
        }
        dummy_json = json.dumps(dummy)
        game_manager.parse_message(dummy_json)

        time.sleep(1)

        dummy["is_accused"] = False
        dummy_json = json.dumps(dummy)
        game_manager.parse_message(dummy_json)

        print(game_manager.json_serialize())
        # [print(player.characterHandler.character.value) for player in game_manager.players]
        await asyncio.get_running_loop().create_future()


if __name__ == "__main__":
    print("Starting clue-less server!")

    # instantiate game

    asyncio.run(main())
