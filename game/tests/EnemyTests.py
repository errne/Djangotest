import unittest
from Enemy import *


class EnemyTests(unittest.TestCase):

    def setUp(self):
        self.enemy = Enemy()

    def test_name(self):
        self.assertEqual(True, len(self.enemy.name) > 3)

    def test_hp_is_above_9(self):
        self.assertEqual(True, self.enemy.hp_count() > 9)

    def test_has_type(self):
        self.assertEqual(True, len(self.enemy.type) > 5)

    def test_random(self):
        self.assertEqual(True, self.enemy.random_for_type < 3)

    def test_attack_damage(self):
        self.assertEqual(True, self.enemy.deal_damage_to_player() >= 3 & self.enemy.deal_damage_to_player() < 26)

    def test_armour_level_above_1(self):
        self.assertEqual(True, self.enemy.armour > 1)

    def test_can_receive_damage(self):
        current_health = self.enemy.hp_count()
        self.enemy.receive_damage(10)
        self.assertEqual(current_health-10+self.enemy.armour, self.enemy.hp_count())

    def test_can_die(self):
        self.enemy.receive_damage(100)
        self.assertEqual(False, self.enemy.is_alive)

