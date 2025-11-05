from .Enemy import Enemy
from .Battle import Battle
import random

def generate_number_of_enemies():
    return random.randint(1, 3)

class Room:
    def __init__(self, player):
        self.number_of_enemies = generate_number_of_enemies()
        self.enemies = []
        self.player = player
        self.treasure_chest = 0
        self.current_enemy_index = 0

    def generate_enemies(self):
        for _ in range(self.number_of_enemies):
            enemy = Enemy()
            self.enemies.append(enemy)

    def add_gold_to_treasure_chest(self):
        amount_to_add = random.randint(10, 25)
        self.treasure_chest += amount_to_add

    def loot_treasure_chest(self):
        if self.player.is_alive:
            gold = self.treasure_chest
            self.player.add_gold_to_pouch(gold)
            self.treasure_chest = 0
            return f"# You found {gold} gold in treasure chest. #\n# Now you have {self.player.gold_pouch} gold in your pouch. #"
        return ""

    def handle_combat_turn(self, choice):
        if not self.enemies:
            self.generate_enemies()

        if self.current_enemy_index >= len(self.enemies):
            return {'text': self.loot_treasure_chest(), 'choices': ["Leave room"]}

        enemy = self.enemies[self.current_enemy_index]
        battle = Battle(self.player, enemy)

        if choice == "Attack":
            result = battle.fight_turn()
            if not self.player.is_alive:
                return {'game_over': True}
            if enemy.hp < 1:
                self.add_gold_to_treasure_chest()
                self.current_enemy_index += 1
                return {'text': result + "\nYou defeated the enemy!", 'choices': ["Next enemy"]}
            return {'text': result, 'choices': ["Attack", "Drink health potion", "Drink attack potion", "Flee"]}
        elif choice == "Drink health potion":
            self.player.drink_health_potion()
            return {'text': f"You now have {self.player.get_health()} HP.", 'choices': ["Attack", "Drink health potion", "Drink attack potion", "Flee"]}
        elif choice == "Drink attack potion":
            self.player.drink_attack_potion()
            return {'text': "You feel stronger!", 'choices': ["Attack", "Drink health potion", "Drink attack potion", "Flee"]}
        elif choice == "Flee":
            return {'text': "You run away!", 'choices': ["Leave room"]}
        else: # First turn
            return {'text': f"You encounter an enemy!\n{enemy.to_string()}", 'choices': ["Attack", "Drink health potion", "Drink attack potion", "Flee"]}
