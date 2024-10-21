import unittest

from weapon import Weapon, WeaponName
from room import Room


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.weapon = Weapon(WeaponName.ROPE)

    def test_init(self):
        self.assertEqual(self.weapon.get_name(), WeaponName.ROPE.value)

    def test_get_enum(self):
        self.assertEqual(self.weapon.get_name_enum(), WeaponName.ROPE)

    def test_set_room(self):
        for room in Room:
            self.weapon.set_room(room)
            self.assertEqual(room, self.weapon.get_room())


if __name__ == '__main__':
    unittest.main()
