import unittest
from Weapon import *
from MaterialTypes import *
from WeaponTypes import *


class WeaponTests(unittest.TestCase):

    def setUp(self):
        self.weapon = Weapon(MaterialTypes.WOOD, WeaponTypes.SWORD)

    def test_max_damage(self):
        self.assertEqual(18, self.weapon.max_damage)

    def test_name(self):
        self.assertEqual("Wood sword", self.weapon.to_string())
