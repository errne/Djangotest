import unittest
from Enemy import *
from Player import *
from Room import *


class EnemyTests(unittest.TestCase):

    def setUp(self):
        self.player = Player("Obi")
        self.room = Room(self.player)

    def test_enemy_count(self):
        self.assertEqual(True, self.room.number_of_enemies > 0)

    def test_enemies(self):
        self.room.generate_enemies()
        self.assertNotEqual([], self.room.enemies)

    def test_room_knows_player_name(self):
        self.assertEqual("Obi", self.room.player.name)

    def test_treasure_chest_starts_with_0(self):
        self.assertEqual(0, self.room.treasure_chest)

    def test_add_gold_to_chest(self):
        self.room.add_gold_to_treasure_chest()
        self.room.add_gold_to_treasure_chest()
        self.assertEqual(True, self.room.treasure_chest >= 20)

    def test_treasure_chest_looting(self):
        self.room.add_gold_to_treasure_chest()
        self.room.loot_treasure_chest()
        self.assertEqual(True, self.room.player.gold_pouch > 9)
        self.assertEqual(0, self.room.treasure_chest)
