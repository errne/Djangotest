import unittest

from Armour import Armour
from ArmourMaterials import ArmourMaterials
from Player import *


class PlayerTests(unittest.TestCase):

    def setUp(self):
        self.player = Player("Obi")
        self.new_weapon = Weapon(MaterialTypes.STEEL, WeaponTypes.BATTLEAXE)
        self.helm = Armour(ArmourMaterials.LEATHER, ArmourTypes.HELM)
        self.helm2 = Armour(ArmourMaterials.MITHRIL, ArmourTypes.HELM)
        self.boots = Armour(ArmourMaterials.STEEL, ArmourTypes.BOOTS)

    def test_name(self):
        self.assertEqual("Obi", self.player.name)

    def test_starting_health(self):
        self.assertEqual(100, self.player.get_health())

    def test_has_3_health_potions_at_start(self):
        self.assertEqual(3, self.player.num_health_pots)

    def test_health_pots_heal(self):
        for _ in range(3):
            self.player.take_damage(15)
        self.player.drink_health_potion()
        self.assertEqual(85, self.player.get_health())

    def test_health_pots_not_heal_when_0(self):
        for _ in range(3):
            self.player.drink_health_potion()
        self.player.take_damage(15)
        self.player.drink_health_potion()
        self.assertEqual(85, self.player.get_health())
        self.assertEqual(0, self.player.num_health_pots)

    def test_can_deal_damage(self):
        self.assertEqual(True, self.player.deal_damage() > 4)

    def test_can_receive_damage(self):
        self.player.take_damage(25)
        self.assertEqual(75, self.player.get_health())

    def test_can_receive_damage_with_armour(self):
        self.player.equip_new_armour(self.helm)
        self.player.equip_new_armour(self.boots)
        self.player.take_damage(15)
        self.assertEqual(91, self.player.get_health())

    def test_drink_attack_potion(self):
        self.player.num_attack_pots += 1
        self.player.drink_attack_potion()
        self.assertEqual(15, self.player.base_attack_damage)
        self.assertEqual(33, self.player.max_attack_damage)

    def test_drink_attack_potion__over_limit(self):
        self.player.num_attack_pots += 10
        for _ in range(9):
            self.player.drink_attack_potion()
        self.assertEqual(45, self.player.base_attack_damage)
        self.assertEqual(63, self.player.max_attack_damage)

    def test_player_starts_with_0_gold(self):
        self.assertEqual(0, self.player.gold_pouch)

    def test_can_add_gold(self):
        self.player.add_gold_to_pouch(25)
        self.assertEqual(25, self.player.gold_pouch)

    def test_player_dies(self):
        self.player.take_damage(125)
        self.assertEqual(False, self.player.is_alive)

    def test_can_equip_new_weapon(self):
        self.player.equip_new_weapon(self.new_weapon)
        self.assertEqual(66, self.player.max_attack_damage)

    def test_buy_new_weapon(self):
        self.player.add_gold_to_pouch(78)
        self.player.buy_weapon(self.new_weapon, 75)
        self.assertEqual(66, self.player.max_attack_damage)
        self.assertEqual(3, self.player.gold_pouch)

    def test_total_armour_level__no_armour(self):
        self.assertEqual(0, self.player.get_total_armour_level())

    def test_total_armour_level_with_some_armour(self):
        self.player.equip_new_armour(self.helm)
        self.player.equip_new_armour(self.boots)
        self.assertEqual(18, self.player.get_total_armour_level())

    def test_equip_armour_over_existing_armour(self):
        self.player.equip_new_armour(self.helm)
        self.player.equip_new_armour(self.boots)
        self.player.equip_new_armour(self.helm2)
        self.assertEqual(23, self.player.get_total_armour_level())

    def test_armour_protection_value(self):
        self.player.equip_new_armour(self.helm)
        self.player.equip_new_armour(self.boots)
        self.player.equip_new_armour(self.helm2)
        self.assertEqual(7, self.player.armour_protection_value())

    def test_inventory_empty_at_beginning(self):
        self.assertEqual(0, len(self.player.inventory))

    def test_add_item_to_inventory(self):
        self.player.add_item_to_inventory(self.helm2)
        self.assertEqual(1, len(self.player.inventory))

    def test_sell_all_inventory(self):
        self.player.add_item_to_inventory(self.helm2)
        self.player.add_item_to_inventory(self.helm2)
        self.assertEqual(2, len(self.player.inventory))
        self.player.sell_all_inventory()
        self.assertEqual(0, len(self.player.inventory))
        self.assertEqual(84, self.player.gold_pouch)

    def test_inventory_checking(self):
        self.player.add_item_to_inventory(self.helm2)
        self.player.add_item_to_inventory(self.helm2)
        self.player.add_item_to_inventory(self.boots)
        item_list = self.player.check_inventory()
        self.assertEqual("Mithril helm, Mithril helm, Steel boots", item_list)







