import random
import logging

from .ArmourTypes import ArmourTypes
from .Reputation import ReputationManager, ReputationLevel
from .Weapon import Weapon
from .MaterialTypes import MaterialTypes
from .WeaponTypes import WeaponTypes

player_logger = logging.getLogger(__name__)

class Player:
    base_attack_damage = 10
    inventory_limit = 24
    def __init__(self, name, game):
        self.__health = 100
        self.__armour_slots = {"Helm": None, "Chest": None, "Trousers": None, "Boots": None}
        self.name = name
        self.game = game
        self.weapon = Weapon(MaterialTypes.WOOD, WeaponTypes.SWORD, image='images/wood_sword.png')
        self.max_attack_damage = self.base_attack_damage + self.weapon.max_damage
        self.inventory = []
        self.gold_pouch = 0
        self.num_health_pots = 3
        self.num_attack_pots = 0
        self.is_alive = True
        self.reputation = {
            "Shopkeepers": None,
            "Mathematicians Guild": None,
            "Thieves Guild": None,
        }
        self.quests = []

    def get_health(self):
        return self.__health

    def set_max_attack_damage(self):
        self.max_attack_damage = self.base_attack_damage + self.weapon.max_damage

    def change_reputation(self, faction, points):
        if self.reputation.get(faction) is None:
            self.reputation[faction] = 0
        
        self.reputation[faction] += points
        # Optional: Add caps to reputation scores if needed
        # e.g., self.reputation[faction] = max(-100, min(100, self.reputation[faction]))

    def get_reputation(self, faction):
        points = self.reputation.get(faction)
        level_name = ReputationManager.get_level_from_points(points)
        return ReputationLevel(level_name)

    def drink_health_potion(self):
        if self.num_health_pots > 0:
            self.health_potion_heal()
            self.num_health_pots -= 1
            if self.num_health_pots <= 0:
                self.num_health_pots = 0
        else:
            self.game.messages.append("\t> You do not have any health potions, defeat enemies for a chance to get one")

    def health_potion_heal(self):
        self.__health += 30
        if self.__health > 100:
            self.__health = 100

    def drink_attack_potion(self):
        if self.num_attack_pots > 0:
            self.attack_potion_boost()
            self.num_attack_pots -= 1
            if self.num_attack_pots <= 0:
                self.num_attack_pots = 0
        else:
            self.game.messages.append("\t> You do not have any attack potions, defeat enemies for a chance to get one")

    def attack_potion_boost(self):
        self.base_attack_damage += 5
        if self.base_attack_damage > 45:
            self.base_attack_damage = 45
            self.game.messages.append("Your maximum damage cannot go any higher")
        self.set_max_attack_damage()

    def deal_damage(self):
        return random.randint(5, self.max_attack_damage)

    def take_damage(self, damage_received):
        damage_received_with_armour = damage_received - self.armour_protection_value()
        if damage_received_with_armour < 1:
            damage_received_with_armour = 0
        self.__health -= damage_received_with_armour
        if self.__health < 1:
            self.is_alive = False
            self.__health = 0

    def add_gold_to_pouch(self, amount_of_gold):
        self.gold_pouch += amount_of_gold

    def buy_weapon(self, weapon, price):
        if price <= self.gold_pouch:
            # Check if we need space for the old weapon
            if self.weapon and len(self.inventory) >= self.inventory_limit:
                 self.game.messages.append("Inventory full! Cannot unequip current weapon.")
                 return

            self.gold_pouch -= price
            self.equip_new_weapon(weapon)
            self.change_reputation("Shopkeepers", ReputationManager.BUY_ITEM)
            player_logger.info(f"Player {self.name} bought {weapon.to_string()}. Shopkeepers reputation changed by {ReputationManager.BUY_ITEM} to {self.reputation['Shopkeepers']} points.")
        else:
            self.game.messages.append("You do not have enough gold for this purchase")
            return

    def sell_item(self, item_index):
        if item_index < len(self.inventory):
            item = self.inventory[item_index]
            self.add_gold_to_pouch(item.price)
            self.inventory.pop(item_index)
            
            self.change_reputation("Shopkeepers", ReputationManager.SELL_ITEM)
            player_logger.info(f"Player {self.name} sold {item.to_string()}. Shopkeepers reputation changed by {ReputationManager.SELL_ITEM} to {self.reputation['Shopkeepers']} points.")
            self.game.messages.append(f"You sold a {item.to_string()} for {item.price} gold.")
        else:
            # This case should ideally be handled by the caller, but as a fallback:
            self.game.messages.append("Invalid item to sell.")

    def equip_new_weapon(self, weapon):
        # If there's an old weapon, put it back in the inventory
        if self.weapon:
            self.inventory.append(self.weapon)
        
        # Remove the new weapon from the inventory if it's there
        if weapon in self.inventory:
            self.inventory.remove(weapon)

        self.weapon = weapon
        self.set_max_attack_damage()
        self.game.messages.append(f"You have equipped {self.weapon.to_string()}")

    def equip_new_armour(self, armour):
        slot_to_equip = None
        if armour.armour_type == ArmourTypes.BOOTS:
            slot_to_equip = "Boots"
        elif armour.armour_type == ArmourTypes.HELM:
            slot_to_equip = "Helm"
        elif armour.armour_type == ArmourTypes.TROUSERS:
            slot_to_equip = "Trousers"
        elif armour.armour_type == ArmourTypes.CHEST:
            slot_to_equip = "Chest"

        if slot_to_equip:
            if self.__armour_slots[slot_to_equip]:
                self.inventory.append(self.__armour_slots[slot_to_equip])
            self.__armour_slots[slot_to_equip] = armour
            self.inventory.remove(armour)

    def get_total_armour_level(self):
        total_armour_value = 0
        for armour in self.__armour_slots:
            if self.__armour_slots[armour] is not None:
                total_armour_value += self.__armour_slots[armour].armour_level
        return total_armour_value

    def armour_protection_value(self):
        armour_protection = self.get_total_armour_level()
        return armour_protection // 3

    def add_item_to_inventory(self, item):
        if len(self.inventory) < self.inventory_limit:
            self.inventory.append(item)
            return True
        else:
            self.game.messages.append("Inventory full!")
            return False

    def sell_all_inventory(self):
        if not self.inventory:
            self.game.messages.append("Your inventory is empty.")
            return
            
        total_income = 0
        num_items_sold = len(self.inventory)
        for item in self.inventory:
            total_income += item.price
        self.add_gold_to_pouch(total_income)
        self.inventory.clear()
        reputation_change = ReputationManager.SELL_ITEM * num_items_sold
        self.change_reputation("Shopkeepers", reputation_change)
        player_logger.info(f"Player {self.name} sold {num_items_sold} items. Shopkeepers reputation changed by {reputation_change} to {self.reputation['Shopkeepers']} points.")
        self.game.messages.append(f"You sold your items and got {total_income} gold")

    def get_armour_from_inventory(self):
        from .Armour import Armour
        return [item for item in self.inventory if isinstance(item, Armour)]

    def get_weapons_from_inventory(self):
        from .Weapon import Weapon
        return [item for item in self.inventory if isinstance(item, Weapon)]

    def check_inventory(self):
        equipped_items = []
        if self.weapon:
            equipped_items.append(self.weapon)
        for armour in self.__armour_slots.values():
            if armour:
                equipped_items.append(armour)
        
        return self.inventory, equipped_items

    def add_quest(self, quest):
        self.quests.append(quest)
        self.game.messages.append(f"Quest Accepted: {quest.name}")

    def has_quest(self, quest_id):
        for quest in self.quests:
            if quest.quest_id == quest_id and not quest.is_completed:
                return True
        return False

    def complete_quest(self, quest_id):
        for quest in self.quests:
            if quest.quest_id == quest_id and not quest.is_completed:
                quest.complete()
                self.add_gold_to_pouch(quest.reward_gold)
                self.game.messages.append(f"Quest Completed: {quest.name}")
                self.game.messages.append(f"You received {quest.reward_gold} gold.")
                return
