import unittest
import json

from card import CharacterCard, WeaponCard, RoomCard
from player import ClueCharacter
from weapon import WeaponName, Weapon
from room import Room


class MyTestCase(unittest.TestCase):
    def test_character_card(self):
        for character in ClueCharacter:
            card = CharacterCard(character)
            self.assertIsInstance(card, CharacterCard)
            self.assertIn(card.get_subject(), ClueCharacter)

    def test_cc_json_serialization(self):
        card = CharacterCard(ClueCharacter.MRS_WHITE)
        json_string = json.dumps(card.dict())
        self.assertEqual(json_string, """{"character_card": "Mrs. White"}""")

    def test_weapon_card(self):
        for name in WeaponName:
            card = WeaponCard(name)
            self.assertIsInstance(card, WeaponCard)
            self.assertIn(card.get_subject().get_name_enum(), WeaponName)

    def test_wc_json_serialization(self):
        card = WeaponCard(WeaponName.ROPE)
        json_string = json.dumps(card.dict())
        self.assertEqual(json_string, """{"weapon_card": "Rope"}""")

    def test_room_card(self):
        for room in Room:
            card = RoomCard(room)
            self.assertIsInstance(card, RoomCard)
            self.assertIn(card.get_subject(), Room)

    def test_rc_json_serialization(self):
        card = RoomCard(Room.BALLROOM)
        json_string = json.dumps(card.dict())
        self.assertEqual(json_string, """{"room_card": "Ballroom"}""")

if __name__ == '__main__':
    unittest.main()
