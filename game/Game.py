import json

from .Armour import Armour
from .ArmourMaterials import ArmourMaterials
from .ArmourTypes import ArmourTypes
from .Player import Player
from .World import World
from .Weapon import Weapon
from .MaterialTypes import MaterialTypes
from .WeaponTypes import WeaponTypes


class Game:

    def __init__(self):
        self.game_is_on = True
        self.player_name = ''

    def display_intro(self):
        print("Do you want to start a new game or load a saved game? (new/load)")
        choice = input().lower()
        if choice == "load":
            player = self.load_game()
            if player:
                self.player_name = player.name
                print(f"Welcome back, {self.player_name}!")
                return player
            else:
                print("Starting a new game as no save file was found.")

        print("Hello there, what is your name?\n")
        self.set_player_name()
        print(f"{self.player_name} your adventure starts here")
        print("Welcome to the dungeon!")
        return self.create_player(self.player_name)

    def set_player_name(self):
        self.player_name = input().capitalize()

    def create_player(self, player_name):
        return Player(player_name)

    def enter_world(self, player):
        world = World(player, self)
        world.display_intro()
        world.travel()

    def save_game(self, player):
        player_data = {
            "name": player.name,
            "health": player.get_health(),
            "armour_slots": {
                slot: {
                    "armour_material": armour.armour_material.name,
                    "armour_type": armour.armour_type.name
                } if armour else None
                for slot, armour in player._Player__armour_slots.items()
            },
            "weapon": {
                "material_type": player.weapon.material_type.name,
                "weapon_type": player.weapon.weapon_type.name
            } if player.weapon else None,
            "base_attack_damage": player.base_attack_damage,
            "num_health_pots": player.num_health_pots,
            "num_attack_pots": player.num_attack_pots,
            "gold_pouch": player.gold_pouch,
            "is_alive": player.is_alive,
            "inventory": [
                {
                    "item_type": "weapon",
                    "material_type": item.material_type.name,
                    "weapon_type": item.weapon_type.name
                } if isinstance(item, Weapon) else {
                    "item_type": "armour",
                    "armour_material": item.armour_material.name,
                    "armour_type": item.armour_type.name
                }
                for item in player.inventory
            ]
        }
        with open("savegame.json", "w") as f:
            json.dump(player_data, f, indent=4)
        print("Game saved!")

    def load_game(self):
        try:
            with open("savegame.json", "r") as f:
                player_data = json.load(f)

            player = Player(player_data["name"])
            player._Player__health = player_data["health"]
            player.base_attack_damage = player_data["base_attack_damage"]
            player.num_health_pots = player_data["num_health_pots"]
            player.num_attack_pots = player_data["num_attack_pots"]
            player.gold_pouch = player_data["gold_pouch"]
            player.is_alive = player_data["is_alive"]

            if player_data["weapon"]:
                weapon_data = player_data["weapon"]
                player.weapon = Weapon(MaterialTypes[weapon_data["material_type"]],
                                        WeaponTypes[weapon_data["weapon_type"]])

            for slot, armour_data in player_data["armour_slots"].items():
                if armour_data:
                    player._Player__armour_slots[slot] = Armour(ArmourMaterials[armour_data["armour_material"]],
                                                                ArmourTypes[armour_data["armour_type"]])

            for item_data in player_data["inventory"]:
                if item_data["item_type"] == "weapon":
                    player.inventory.append(Weapon(MaterialTypes[item_data["material_type"]],
                                                    WeaponTypes[item_data["weapon_type"]]))
                elif item_data["item_type"] == "armour":
                    player.inventory.append(Armour(ArmourMaterials[item_data["armour_material"]],
                                                    ArmourTypes[item_data["armour_type"]]))

            player.set_max_attack_damage()
            print("Game loaded!")
            return player
        except FileNotFoundError:
            print("No save file found.")
            return None
