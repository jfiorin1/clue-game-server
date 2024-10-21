import unittest

from clueMap import ClueMap
from gameManager import gameManager


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.map = ClueMap()

    def test_player_map(self):
        for player in gameManager.players:
            coordinates = player.get_position()
            self.assertEqual(self.map.get_player_map()[coordinates[0]][coordinates[1]], player)

    def test_weapons_map(self):
        for weapon in gameManager.weapons:
            self.assertEqual(self.map.get_weapons_map()[weapon].name, weapon.get_room().name)


if __name__ == '__main__':
    unittest.main()
