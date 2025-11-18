import unittest
from game.Player import *
from game.Shop import *
from game.Armour import *
from game.ArmourMaterials import *
from game.Weapon import Weapon
from game.MaterialTypes import MaterialTypes
from game.WeaponTypes import WeaponTypes
from game.ArmourTypes import ArmourTypes


class MockGame:
    def __init__(self):
        self.messages = []

class ShopTests(unittest.TestCase):

    def setUp(self):
        self.game = MockGame()
        self.player = Player("Obi", self.game)
        self.shop = Shop("Dragonwares", self.game)
        self.item1 = Weapon(MaterialTypes.STEEL, WeaponTypes.BATTLEAXE)
        self.item2 = Armour(ArmourMaterials.MITHRIL, ArmourTypes.HELM)

    def test_has_name(self):
        self.assertEqual("Dragonwares", self.shop.name)

    def test_weapon_stock(self):
        self.assertEqual(16, len(self.shop.weapons))

    def test_player_can_equip_weapon_from_list(self):
        self.player.equip_new_weapon(self.shop.weapons[3])
        self.assertEqual(31, self.player.max_attack_damage)

    def test_player_selling_all_inventory(self):
        self.player.add_item_to_inventory(self.item1)
        self.player.add_item_to_inventory(self.item2)
        self.player.sell_all_inventory()
        self.assertEqual(154, self.player.gold_pouch)

    def test_player_selling_particular_item(self):
        self.player.add_item_to_inventory(self.item1)
        self.player.add_item_to_inventory(self.item2)
        self.player.sell_item(1)
        self.assertEqual(42, self.player.gold_pouch)
        self.assertEqual(1, len(self.player.inventory))
