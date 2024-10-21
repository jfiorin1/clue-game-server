import unittest
import json

from card import CharacterCard, WeaponCard, RoomCard
from player import Player, ClueCharacter
from room import Room
from weapon import Weapon, WeaponName


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.player = Player("test", ClueCharacter.MRS_WHITE)

    def test_str(self):
        self.assertEqual(str(self.player), "test : " + ClueCharacter.MRS_WHITE.name)

    def test_set_position(self):
        self.player.set_position(0, 0)
        self.assertEqual(self.player.position, (0,0))

    def test_add_card(self):
        card = CharacterCard(ClueCharacter.MISS_SCARLETT)
        self.player.add_cards([card])
        self.assertIn(card, self.player.get_cards())

    def test_add_note(self):
        self.player.add_note("test")
        self.assertEqual(self.player.notes, "test")

    def test_empty_json_serialization(self):
        self.assertEqual(json.dumps(self.player.dict()),
                         """{"name": "test", "character": "Mrs. White", "position": {"x": 0, "y": 0}, "cards": [], "notes": "", "is_active": true}""")

    def test_json_serialization(self):
        self.player = Player("test2", ClueCharacter.MISS_SCARLETT)
        self.player.set_position(1, 1)

        card1 = CharacterCard(ClueCharacter.MISS_SCARLETT)
        card2 = WeaponCard(Weapon(WeaponName.ROPE, Room.HALL))
        card3 = RoomCard(Room.BALLROOM)

        self.player.add_cards([card1, card2, card3])
        self.player.add_note("notes")
        self.assertEqual(json.dumps(self.player.dict()),
                         """{"name": "test2", "character": "Miss Scarlett", "position": {"x": 1, "y": 1}, "cards": [{"character_card": "Miss Scarlett"}, {"weapon_card": "Rope"}, {"room_card": "Ballroom"}], "notes": "notes", "is_active": true}""")

    @unittest.skip("not yet implemented")
    def test_default_position(self):
        for character in ClueCharacter:
            self.assertEqual(character.get_default_position(), None)


if __name__ == '__main__':
    unittest.main()
