import unittest
import os
import json
from Game import Game
from Player import Player
from Weapon import Weapon
from Armour import Armour
from MaterialTypes import MaterialTypes
from WeaponTypes import WeaponTypes
from ArmourTypes import ArmourTypes
from ArmourMaterials import ArmourMaterials

class GameTests(unittest.TestCase):

    def setUp(self):
        self.game = Game()
        self.player = Player("Test Player")
        self.player.gold_pouch = 100
        self.player.num_health_pots = 5
        self.player.weapon = Weapon(MaterialTypes.STEEL, WeaponTypes.SWORD)
        self.player.inventory.append(Armour(ArmourMaterials.LEATHER, ArmourTypes.CHEST))

    def tearDown(self):
        if os.path.exists("savegame.json"):
            os.remove("savegame.json")

    def test_save_and_load_game(self):
        # Save the game
        self.game.save_game(self.player)

        # Load the game
        loaded_player = self.game.load_game()

        # Check that the loaded player is not None
        self.assertIsNotNone(loaded_player)

        # Check that the loaded player's attributes match the original player's attributes
        self.assertEqual(self.player.name, loaded_player.name)
        self.assertEqual(self.player.get_health(), loaded_player.get_health())
        self.assertEqual(self.player.gold_pouch, loaded_player.gold_pouch)
        self.assertEqual(self.player.num_health_pots, loaded_player.num_health_pots)
        self.assertEqual(self.player.weapon.to_string(), loaded_player.weapon.to_string())
        self.assertEqual(len(self.player.inventory), len(loaded_player.inventory))
        self.assertEqual(self.player.inventory[0].to_string(), loaded_player.inventory[0].to_string())

if __name__ == '__main__':
    unittest.main()
