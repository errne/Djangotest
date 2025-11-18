import unittest
import os
import json
from game.Game import Game
from game.Player import Player
from game.Weapon import Weapon
from game.Armour import Armour
from game.MaterialTypes import MaterialTypes
from game.WeaponTypes import WeaponTypes
from game.ArmourTypes import ArmourTypes
from game.ArmourMaterials import ArmourMaterials

class GameTests(unittest.TestCase):

    def setUp(self):
        self.game = Game()
        self.player = Player("Test Player", self.game)
        self.player.gold_pouch = 100
        self.player.num_health_pots = 5
        self.player.weapon = Weapon(MaterialTypes.STEEL, WeaponTypes.SWORD)
        self.player.inventory.append(Armour(ArmourMaterials.LEATHER, ArmourTypes.CHEST))



if __name__ == '__main__':
    unittest.main()
