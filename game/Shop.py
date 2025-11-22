from .MaterialTypes import MaterialTypes
from .Weapon import Weapon
from .WeaponTypes import WeaponTypes

class Shop:
    def __init__(self, name, game):
        self.name = name
        self.game = game
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
        self.game.messages.append(f"Welcome to {self.name}! What would you like to do?")
        return {
            'choices': ["Buy", "Sell", "Leave"]
        }

    def get_buy_menu(self):
        choices = [f"Buy {w.to_string()} for {w.max_damage * 3} gold" for w in self.weapons]
        choices.append("Back to main menu")
        self.game.messages.append("Take a look at my wares.")
        return {
            'choices': choices
        }

    def get_sell_menu(self, player):
        if not player.inventory:
            self.game.messages.append("You have nothing to sell.")
            return {'choices': ["Back to main menu"]}
        
        choices = [f"Sell {item.to_string()} for {item.price} gold" for item in player.inventory]
        choices.append("Back to main menu")
        self.game.messages.append("What do you want to sell?")
        return {
            'choices': choices
        }

    def buy_item(self, player, item_index):
        if item_index < len(self.weapons):
            weapon = self.weapons[item_index]
            price = weapon.max_damage * 3
            
            # Check if player has space for old weapon (if any)
            # Player.buy_weapon handles this check now, but we can duplicate it here for better UX or rely on Player
            # Player.buy_weapon returns None, so we can't check return value easily unless we modify it.
            # But Player.buy_weapon appends a message if it fails.
            
            if player.gold_pouch >= price:
                # We can check limit here too
                if player.weapon and len(player.inventory) >= player.inventory_limit:
                     self.game.messages.append("Inventory full! Cannot unequip current weapon.")
                     return

                player.buy_weapon(weapon, price)
                # We should only append "You bought..." if it succeeded.
                # Since we checked the condition above, it should succeed unless something else is wrong.
                # But wait, player.buy_weapon appends "You have equipped..."
                # We can append "You bought..." here.
                self.game.messages.append(f"You bought a {weapon.to_string()}")
            else:
                self.game.messages.append("You don't have enough gold.")
        else:
            self.game.messages.append("Invalid item.")

    def sell_item(self, player, item_index):
        if item_index < len(player.inventory):
            player.sell_item(item_index)
        else:
            self.game.messages.append("Invalid item.")
