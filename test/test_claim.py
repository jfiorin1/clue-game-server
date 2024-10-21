import unittest
import json

from claim import Suggestion, Accuse
from player import ClueCharacter
from weapon import Weapon, WeaponName
from room import Room


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.character = ClueCharacter.MISS_SCARLETT
        self.weapon = Weapon(WeaponName.ROPE)
        self.room = Room.BILLIARD

    def test_init_suggestion(self):
        suggestion = Suggestion(self.character, self.weapon, self.room)
        self.assertEqual(suggestion.make_string(), "I suggest it was Miss Scarlett with the Rope in the Billiard Room")

    def test_suggestion_json(self):
        suggestion = Suggestion(self.character, self.weapon, self.room)
        self.assertEqual(json.dumps(suggestion.dict()), """{"suggestion": {"character": "MISS_SCARLETT", "weapon": "ROPE", "room": "BILLIARD"}}""")

    def test_init_accusation(self):
        accusation = Accuse(self.character, self.weapon, self.room)
        self.assertEqual(accusation.make_string(), "I accuse Miss Scarlett with the Rope in the Billiard Room")

    def test_accusation_json(self):
        accusation = Accuse(self.character, self.weapon, self.room)
        self.assertEqual(json.dumps(accusation.dict()), """{"accusation": {"character": "MISS_SCARLETT", "weapon": "ROPE", "room": "BILLIARD"}}""")


if __name__ == '__main__':
    unittest.main()
