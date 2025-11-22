from .Room import Room
from .EnemyThief import ThiefEnemy
import random

class ThievesDen(Room):
    def __init__(self, player, game):
        super().__init__(player, game)
        self.name = "Thieves Den"

    def generate_enemies(self):
        for _ in range(self.number_of_enemies):
            enemy = ThiefEnemy()
            self.enemies.append(enemy)

    def loot_treasure_chest(self):
        if self.player.is_alive:
            # Check for quest item
            if self.player.has_quest("retrieve_heirloom"):
                 self.game.messages.append("You found the Stolen Heirloom in the chest!")
                 self.player.complete_quest("retrieve_heirloom")
            
            super().loot_treasure_chest()
