import unittest
from game.Enemy import *
from game.Player import *
from game.Room import *


class MockGame:
    def __init__(self):
        self.messages = []

class RoomTests(unittest.TestCase):

    def setUp(self):
        self.game = MockGame()
        self.player = Player("Obi", self.game)
        self.room = Room(self.player, self.game)

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
