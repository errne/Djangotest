import unittest
from game.Armour import *
from game.ArmourMaterials import ArmourMaterials
from game.ArmourTypes import ArmourTypes


class ArmourTests(unittest.TestCase):

    def setUp(self):
        self.armour = Armour(ArmourMaterials.STEEL, ArmourTypes.HELM)

    def test_armour_level(self):
        self.assertEqual(12, self.armour.armour_level)

    def test_print_name(self):
        self.assertEqual("Steel helm", self.armour.to_string())

    def test_has_price(self):
        self.assertEqual(36, self.armour.price)
