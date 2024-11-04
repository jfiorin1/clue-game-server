import json
import unittest

from claim import Suggestion, Accuse
from claimsLog import ClaimsLog
from player import ClueCharacter
from room import Room
from weapon import Weapon, WeaponName


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.log = ClaimsLog()

    def test_empty_log(self):
        self.assertEqual(json.dumps(self.log.array_of_claims_dicts()), "[]")

    def test_add_claim(self):
        character = ClueCharacter.MISS_SCARLETT
        weapon = Weapon(WeaponName.ROPE)
        room = Room.CONSERVATORY

        suggestion = Suggestion(character, weapon, room)
        accuse = Accuse(character, weapon, room)

        self.log.add_claim(suggestion)
        self.log.add_claim(accuse)

        self.assertEqual(json.dumps(self.log.array_of_claims_dicts()),
                         """[{"suggestion": {"character": "MISS_SCARLETT", "weapon": "ROPE", "room": "CONSERVATORY"}}, {"accusation": {"character": "MISS_SCARLETT", "weapon": "ROPE", "room": "CONSERVATORY"}}]""")

if __name__ == '__main__':
    unittest.main()
