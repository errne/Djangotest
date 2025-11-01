from .MaterialTypes import MaterialTypes
from .Weapon import Weapon
from .WeaponTypes import WeaponTypes

class Shop:
    def __init__(self, name):
        self.name = name
        self.weapons = self.generate_weapons_stock()

    def generate_weapons_stock(self):
        weapons_stock = []
        material_list = MaterialTypes.create_list(self)
        weapons_list = WeaponTypes.create_list(self)
        for material in material_list:
            for weapon_type in weapons_list:
                weapon = Weapon(material, weapon_type)
                weapons_stock.append(weapon)
        return weapons_stock

    def get_shop_menu(self):
        return {
            'text': f"Welcome to {self.name}! What would you like to do?",
            'choices': ["Buy", "Sell", "Leave"]
        }

    def get_buy_menu(self):
        choices = [f"Buy {w.to_string()} for {w.max_damage * 3} gold" for w in self.weapons]
        choices.append("Back to main menu")
        return {
            'text': "Take a look at my wares.",
            'choices': choices
        }

    def get_sell_menu(self, player):
        if not player.inventory:
            return {'text': "You have nothing to sell.", 'choices': ["Back to main menu"]}
        
        choices = [f"Sell {item.to_string()} for {item.price} gold" for item in player.inventory]
        choices.append("Back to main menu")
        return {
            'text': "What do you want to sell?",
            'choices': choices
        }

    def buy_item(self, player, item_index):
        if item_index < len(self.weapons):
            weapon = self.weapons[item_index]
            price = weapon.max_damage * 3
            if player.gold_pouch >= price:
                player.buy_weapon(weapon, price)
                return f"You bought a {weapon.to_string()}"
            else:
                return "You don't have enough gold."
        return "Invalid item."

    def sell_item(self, player, item_index):
        if item_index < len(player.inventory):
            item = player.inventory[item_index]
            player.add_gold_to_pouch(item.price)
            player.inventory.pop(item_index)
            return f"You sold a {item.to_string()} for {item.price} gold."
        return "Invalid item."
