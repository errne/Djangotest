from abc import ABC, abstractmethod
from .Shop import Shop
from .Room import Room
from .RandomEvent import RandomEvent

class BaseState(ABC):
    def __init__(self, world):
        self.world = world

    @abstractmethod
    def get_scene(self):
        pass

    @abstractmethod
    def handle_choice(self, choice_index):
        pass

class RoadState(BaseState):
    def get_scene(self):
        self.world.game.messages.append("You are on the road.")
        return {
            'choices': ["Continue traveling", "Check inventory", "Equip", "Save and quit"]
        }

    def handle_choice(self, choice_index):
        if choice_index == 0:  # Continue traveling
            return self.world.generate_next_stop()
        elif choice_index == 1:  # Check inventory
            inventory, equipped = self.world.player.check_inventory()
            self.world.game.messages.append("Inventory:")
            for item in inventory:
                self.world.game.messages.append(item.to_string())
            self.world.game.messages.append("Equipped:")
            for item in equipped:
                self.world.game.messages.append(item.to_string())
            return {'choices': ["Back to road"]}
        elif choice_index == 2:  # Equip - now goes to EquipState menu
            self.world.current_state = EquipState(self.world, mode='item_type_selection')
            return self.world.get_current_scene()
        elif choice_index == 3:  # Save and quit
            self.world.game.messages.append("Game saved. Thanks for playing!")
            return {'choices': []}
        elif choice_index == 0 and self.world.game.messages and self.world.game.messages[-1] == "Equipped:":
            return self.get_scene()
        return self.world.get_current_scene()

class EquipState(BaseState):
    def __init__(self, world, mode='item_type_selection'):
        super().__init__(world)
        self.mode = mode # 'item_type_selection', 'armour', 'weapon'

    def get_scene(self):
        if self.mode == 'item_type_selection':
            self.world.game.messages.append("What type of item do you want to equip?")
            return {'choices': ["Equip Armour", "Equip Weapon", "Back to Road"]}
        elif self.mode == 'armour':
            armour_list = self.world.player.get_armour_from_inventory()
            if not armour_list:
                self.world.game.messages.append("You have no armour to equip.")
                self.mode = 'item_type_selection' # Go back to item type selection menu
                return self.get_scene()
            
            choices = [f"Equip {armour.to_string()}" for armour in armour_list]
            choices.append("Back to Item Type Selection")
            self.world.game.messages.append("Choose armour to equip:")
            return {'choices': choices}
        elif self.mode == 'weapon':
            weapon_list = self.world.player.get_weapons_from_inventory()
            if not weapon_list:
                self.world.game.messages.append("You have no weapons to equip.")
                self.mode = 'item_type_selection' # Go back to item type selection menu
                return self.get_scene()
            
            choices = [f"Equip {weapon.to_string()}" for weapon in weapon_list]
            choices.append("Back to Item Type Selection")
            self.world.game.messages.append("Choose weapon to equip:")
            return {'choices': choices}

    def handle_choice(self, choice_index):
        if self.mode == 'item_type_selection':
            if choice_index == 0: # Equip Armour
                self.mode = 'armour'
                return self.get_scene()
            elif choice_index == 1: # Equip Weapon
                self.mode = 'weapon'
                return self.get_scene()
            elif choice_index == 2: # Back to Road
                self.world.current_state = RoadState(self.world)
                return self.world.get_current_scene()
        elif self.mode == 'armour':
            armour_list = self.world.player.get_armour_from_inventory()
            if choice_index == len(armour_list): # Back to Item Type Selection
                self.mode = 'item_type_selection'
                return self.get_scene()
            else:
                armour_to_equip = armour_list[choice_index]
                self.world.player.equip_new_armour(armour_to_equip)
                self.world.game.messages.append(f"You have equipped {armour_to_equip.to_string()}.")
                self.mode = 'item_type_selection' # Go back to item type selection menu after equipping
                return self.get_scene()
        elif self.mode == 'weapon':
            weapon_list = self.world.player.get_weapons_from_inventory()
            if choice_index == len(weapon_list): # Back to Item Type Selection
                self.mode = 'item_type_selection'
                return self.get_scene()
            else:
                weapon_to_equip = weapon_list[choice_index]
                self.world.player.equip_new_weapon(weapon_to_equip)
                self.mode = 'item_type_selection' # Go back to item type selection menu after equipping
                return self.get_scene()

class ShopState(BaseState):
    def __init__(self, world, shop_event: Shop, sub_location=None):
        super().__init__(world)
        self.shop_event = shop_event
        self.sub_location = sub_location # 'buy', 'sell', or None (main menu)

    def get_scene(self):
        if self.sub_location == 'buy':
            return self.shop_event.get_buy_menu()
        elif self.sub_location == 'sell':
            return self.shop_event.get_sell_menu(self.world.player)
        else: # Main menu
            return self.shop_event.get_shop_menu()

    def handle_choice(self, choice_index):
        if self.sub_location is None: # Main menu
            if choice_index == 0: # Buy
                self.sub_location = 'buy'
                return self.get_scene()
            elif choice_index == 1: # Sell
                self.sub_location = 'sell'
                return self.get_scene()
            else: # Leave
                self.world.current_state = RoadState(self.world)
                return self.world.get_current_scene()
        elif self.sub_location == 'buy':
            if choice_index == len(self.shop_event.weapons): # Back to main menu
                self.sub_location = None
                return self.get_scene()
            else:
                self.shop_event.buy_item(self.world.player, choice_index)
                return self.get_scene() # Stay in buy menu
        elif self.sub_location == 'sell':
            # Check if player inventory is empty before trying to access len(self.world.player.inventory)
            # and also handle the "Back to main menu" choice
            if not self.world.player.inventory or choice_index == len(self.world.player.inventory):
                self.sub_location = None
                return self.get_scene()
            else:
                self.shop_event.sell_item(self.world.player, choice_index)
                return self.get_scene() # Stay in sell menu

class RoomState(BaseState):
    def __init__(self, world, room_event: Room):
        super().__init__(world)
        self.room_event = room_event

    def get_scene(self):
        return self.room_event.handle_combat_turn(None) # Get initial combat scene

    def handle_choice(self, choice_index):
        scene = self.room_event.handle_combat_turn(None) # Get current combat scene state
        if scene.get('game_over'):
            return scene # Game over, no further choices

        choice = scene['choices'][choice_index]
        scene = self.room_event.handle_combat_turn(choice)

        if scene.get('game_over'):
            return scene
        if scene.get('cleared_room'):
            self.world.current_state = ClearedRoomState(self.world) # Transition to ClearedRoomState
            return self.world.get_current_scene()
        if scene['choices'] == ["Leave room"]:
            self.world.current_state = RoadState(self.world) # Transition to RoadState
            return self.world.get_current_scene()
        return scene # Stay in RoomState, return updated scene

class ClearedRoomState(BaseState):
    def get_scene(self):
        self.world.game.messages.append("You have cleared the cavern.")
        return {
            'choices': ["Continue traveling", "Check inventory", "Equip"]
        }

    def handle_choice(self, choice_index):
        if choice_index == 0:  # Continue traveling
            self.world.current_state = RoadState(self.world)
            return self.world.generate_next_stop()
        elif choice_index == 1:  # Check inventory
            inventory, equipped = self.world.player.check_inventory()
            self.world.game.messages.append("Inventory:")
            for item in inventory:
                self.world.game.messages.append(item.to_string())
            self.world.game.messages.append("Equipped:")
            for item in equipped:
                self.world.game.messages.append(item.to_string())
            return self.get_scene() # Stay in ClearedRoomState after checking inventory
        elif choice_index == 2:  # Equip - now goes to EquipState menu
            self.world.current_state = EquipState(self.world, mode='item_type_selection')
            return self.world.get_current_scene()

class EventState(BaseState):
    def __init__(self, world, random_event: RandomEvent):
        super().__init__(world)
        self.random_event = random_event

    def get_scene(self):
        self.world.game.messages.append(self.random_event.event_greeting())
        return self.random_event.event_task()

    def handle_choice(self, choice_index):
        choice = self.random_event.get_choices()[choice_index]
        self.random_event.check_answer(choice)
        self.world.current_state = RoadState(self.world) # Transition back to RoadState after event
        return self.world.get_current_scene()