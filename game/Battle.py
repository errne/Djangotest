import random

from .Armour import Armour
from .ArmourMaterials import ArmourMaterials
from .ArmourTypes import ArmourTypes

class Battle:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.health_potion_drop_chance = 95
        self.attack_potion_drop_chance = 25
        self.armour_drop_chance = 75

    def fight_turn(self):
        damage_dealt = self.player.deal_damage()
        self.enemy.receive_damage(damage_dealt)
        damage_taken = self.enemy.deal_damage_to_player()
        self.player.take_damage(damage_taken)

        result = f"> You strike the {self.enemy.name} for {damage_dealt} damage\n"
        result += f"> You received {damage_taken} in retaliation"

        if not self.player.is_alive:
            result += "\n> You have taken too much damage, you are too weak to go on"
        elif not self.enemy.is_alive:
            result += self.aftermath()

        return result

    def loot_drop(self):
        loot_result = ""
        if random.randint(1, 100) < self.health_potion_drop_chance:
            loot_result += f"# The {self.enemy.name} dropped a health potion. #\n"
            self.player.num_health_pots += 1
            loot_result += f"# You now have {self.player.num_health_pots} health potion(s). #\n"

        if random.randint(1, 100) < self.attack_potion_drop_chance:
            loot_result += f"# The {self.enemy.name} dropped a attack potion. #\n"
            self.player.num_attack_pots += 1
            loot_result += f"# You now have {self.player.num_attack_pots} attack potion(s). #\n"

        if random.randint(1, 100) < self.armour_drop_chance:
            armour = self.generate_drop()
            loot_result += f"# The {self.enemy.name} dropped a {armour.to_string()}. #\n"
            self.player.add_item_to_inventory(armour)
        return loot_result

    def aftermath(self):
        if not self.player.is_alive:
            return "> You have been defeated"
        elif not self.enemy.is_alive:
            result = f"# {self.enemy.name} was defeated! #\n"
            result += f"# You have {self.player.get_health()}HP left #\n"
            result += self.loot_drop()
            return result
        else:
            return "> You fled the battle you coward"

    def generate_drop(self):
        armour_type = random.choice(ArmourTypes.create_list(self))
        armour_material = random.choice([ArmourMaterials.LEATHER, ArmourMaterials.CLOTH])
        return Armour(armour_material, armour_type)
