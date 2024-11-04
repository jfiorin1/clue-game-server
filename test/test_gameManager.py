import unittest

from gameManager import GameManager
from player import Player, ClueCharacter


class MyTestCase(unittest.TestCase):
    def test_empty_game(self):
        game_manager = GameManager()
        self.assertEqual(game_manager.json_serialize(),
                         """{"players": [], "weapons": [{"name": "Candlestick", "room": null}, {"name": "Dagger", "room": null}, {"name": "Lead Pipe", "room": null}, {"name": "Revolver", "room": null}, {"name": "Rope", "room": null}, {"name": "Wrench", "room": null}], "claims": []}""")

    def test_game(self):
        player1 = Player("player1", ClueCharacter.MISS_SCARLETT)
        player2 = Player("player2", ClueCharacter.MRS_WHITE)
        player3 = Player("player3", ClueCharacter.PROFESSOR_PLUM)

        game_manager = GameManager([player1, player2, player3])
        self.assertEqual(game_manager.json_serialize(),
                         """{"players": [{"name": "player1", "character": "Miss Scarlett", "position": {"x": 0, "y": 0}, "cards": [], "notes": "", "is_active": true}, {"name": "player2", "character": "Mrs. White", "position": {"x": 0, "y": 0}, "cards": [], "notes": "", "is_active": true}, {"name": "player3", "character": "Professor Plum", "position": {"x": 0, "y": 0}, "cards": [], "notes": "", "is_active": true}], "weapons": [{"name": "Candlestick", "room": null}, {"name": "Dagger", "room": null}, {"name": "Lead Pipe", "room": null}, {"name": "Revolver", "room": null}, {"name": "Rope", "room": null}, {"name": "Wrench", "room": null}], "claims": []}""")

    @unittest.skip("not yet implemented")
    def test_next_phase(self):
        pass

    @unittest.skip("not yet implemented")
    def test_next_player(self):
        pass

if __name__ == '__main__':
    unittest.main()
