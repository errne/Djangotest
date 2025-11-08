import random

from .Armour import Armour
from .ArmourMaterials import ArmourMaterials
from .ArmourTypes import ArmourTypes

from .Weapon import Weapon
from .MaterialTypes import MaterialTypes
from .WeaponTypes import WeaponTypes

class Battle:
    def __init__(self, player, enemy, game):
        self.player = player
        self.enemy = enemy
        self.game = game
        self.health_potion_drop_chance = 95
        self.attack_potion_drop_chance = 25
        self.armour_drop_chance = 75
        self.weapon_drop_chance = 50

    def fight_turn(self):
        damage_dealt = self.player.deal_damage()
        self.enemy.receive_damage(damage_dealt)
        damage_taken = self.enemy.deal_damage_to_player()
        self.player.take_damage(damage_taken)

        self.game.messages.append(f"> You strike the {self.enemy.name} for {damage_dealt} damage")
        self.game.messages.append(f"> You received {damage_taken} in retaliation")

        if not self.player.is_alive:
            self.game.messages.append("> You have taken too much damage, you are too weak to go on")
        elif not self.enemy.is_alive:
            self.aftermath()

    def loot_drop(self):
        if random.randint(1, 100) < self.health_potion_drop_chance:
            self.game.messages.append(f"# The {self.enemy.name} dropped a health potion. #")
            self.player.num_health_pots += 1
            self.game.messages.append(f"# You now have {self.player.num_health_pots} health potion(s). #")

        if random.randint(1, 100) < self.attack_potion_drop_chance:
            self.game.messages.append(f"# The {self.enemy.name} dropped a attack potion. #")
            self.player.num_attack_pots += 1
            self.game.messages.append(f"# You now have {self.player.num_attack_pots} attack potion(s). #")

        if random.randint(1, 100) < self.weapon_drop_chance:
            weapon = self.generate_weapon_drop()
            self.game.messages.append(f"# The {self.enemy.name} dropped a {weapon.to_string()}. #")
            self.player.add_item_to_inventory(weapon)
        elif random.randint(1, 100) < self.armour_drop_chance:
            armour = self.generate_drop()
            self.game.messages.append(f"# The {self.enemy.name} dropped a {armour.to_string()}. #")
            self.player.add_item_to_inventory(armour)

    def aftermath(self):
        if not self.player.is_alive:
            self.game.messages.append("> You have been defeated")
        elif not self.enemy.is_alive:
            self.game.messages.append(f"# {self.enemy.name} was defeated! #")
            self.game.messages.append(f"# You have {self.player.get_health()}HP left #")
            self.loot_drop()
        else:
            self.game.messages.append("> You fled the battle you coward")

    def generate_drop(self):
        armour_type = random.choice(ArmourTypes.create_list(self))
        armour_material = random.choice([ArmourMaterials.LEATHER, ArmourMaterials.CLOTH])
        return Armour(armour_material, armour_type)

    def generate_weapon_drop(self):
        # Testing drop with images
        weapon_material= random.choice([MaterialTypes.WOOD, MaterialTypes.IRON, MaterialTypes.STEEL, MaterialTypes.MITHRIL])
        weapon_image = f'images/{weapon_material.name.lower()}_sword.png'
        return Weapon(weapon_material, WeaponTypes.SWORD, image=weapon_image)
