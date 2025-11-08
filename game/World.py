import random
from .RandomEvent import RandomEvent
from .Room import Room
from .Shop import Shop

class World:
    def __init__(self, player, game):
        self.player = player
        self.game = game
        self.current_location = None  # Can be 'room', 'shop', 'event', or None
        self.current_sub_location = None
        self.current_event = None

    def get_current_scene(self):
        if self.current_location is None:
            self.game.messages.append("You are on the road.")
            return {
                'choices': ["Continue traveling", "Check inventory", "Equip armour", "Save and quit"]
            }
        elif self.current_location == 'shop':
            shop = self.current_event
            if self.current_sub_location == 'buy':
                return shop.get_buy_menu()
            elif self.current_sub_location == 'sell':
                return shop.get_sell_menu(self.player)
            else:
                return shop.get_shop_menu()
        elif self.current_location == 'room':
            room = self.current_event
            return room.handle_combat_turn(None) # Get initial combat scene
        elif self.current_location == 'cleared_room':
            self.game.messages.append("You have cleared the cavern.")
            return {
                'choices': ["Continue traveling", "Check inventory", "Equip armour"]
            }
        elif self.current_location == 'equip':
            armour_list = self.player.get_armour_from_inventory()
            if not armour_list:
                self.game.messages.append("You have no armour to equip.")
                self.current_location = None
                return self.get_current_scene()
            
            choices = [f"Equip {armour.to_string()}" for armour in armour_list]
            choices.append("Back to road")
            self.game.messages.append("What do you want to equip?")
            return {'choices': choices}
        elif self.current_location == 'event':
            event = self.current_event
            self.game.messages.append(event.event_greeting())
            return event.event_task()

    def handle_choice(self, choice_index):
        if self.current_location is None:
            if choice_index == 0:  # Continue traveling
                return self.generate_next_stop()
            elif choice_index == 1:  # Check inventory
                inventory, equipped = self.player.check_inventory()
                self.game.messages.append("Inventory:")
                for item in inventory:
                    self.game.messages.append(item.to_string())
                self.game.messages.append("Equipped:")
                for item in equipped:
                    self.game.messages.append(item.to_string())
                return {'choices': ["Back to road"]}
            elif choice_index == 2:  # Equip armour
                self.current_location = 'equip'
                return self.get_current_scene()
            elif choice_index == 3:  # Save and quit
                self.game.messages.append("Game saved. Thanks for playing!")
                return {'choices': []}
        elif self.current_location == 'shop':
            shop = self.current_event
            if self.current_sub_location is None: # Main menu
                if choice_index == 0: # Buy
                    self.current_sub_location = 'buy'
                    return shop.get_buy_menu()
                elif choice_index == 1: # Sell
                    self.current_sub_location = 'sell'
                    return shop.get_sell_menu(self.player)
                else: # Leave
                    self.current_location = None
                    self.current_sub_location = None
                    return self.get_current_scene()
            elif self.current_sub_location == 'buy':
                if choice_index == len(shop.weapons): # Back to main menu
                    self.current_sub_location = None
                    return shop.get_shop_menu()
                else:
                    shop.buy_item(self.player, choice_index)
                    return {'choices': shop.get_buy_menu()['choices']}
            elif self.current_sub_location == 'sell':
                if not self.player.inventory or choice_index == len(self.player.inventory): # Back to main menu
                    self.current_sub_location = None
                    return shop.get_shop_menu()
                else:
                    shop.sell_item(self.player, choice_index)
                    return {'choices': shop.get_sell_menu(self.player)['choices']}
        elif self.current_location == 'room':
            room = self.current_event
            scene = room.handle_combat_turn(None)
            if scene.get('game_over'):
                return scene
            choice = scene['choices'][choice_index]
            scene = room.handle_combat_turn(choice)
            if scene.get('game_over'):
                return scene
            if scene.get('cleared_room'):
                self.current_location = 'cleared_room'
                return self.get_current_scene()
            if scene['choices'] == ["Leave room"]:
                self.current_location = None
            return scene
        elif self.current_location == 'cleared_room':
            if choice_index == 0:  # Continue traveling
                self.current_location = None
                return self.generate_next_stop()
            elif choice_index == 1:  # Check inventory
                self.game.messages.append(self.player.check_inventory())
                return {'choices': ["Continue traveling", "Check inventory", "Equip armour"]}
            elif choice_index == 2:  # Equip armour
                self.current_location = 'equip'
                return self.get_current_scene()
        elif self.current_location == 'equip':
            armour_list = self.player.get_armour_from_inventory()
            if choice_index == len(armour_list): # Back to road
                self.current_location = None
                return self.get_current_scene()
            else:
                armour_to_equip = armour_list[choice_index]
                self.player.equip_new_armour(armour_to_equip)
                self.game.messages.append(f"You have equipped {armour_to_equip.to_string()}.")
                self.current_location = None
                return self.get_current_scene()
        elif self.current_location == 'event':
            event = self.current_event
            choice = event.get_choices()[choice_index]
            event.check_answer(choice)
            self.current_location = None
            return {'choices': ["Continue traveling"]}

    def generate_next_stop(self):
        random_no = random.randint(1, 100)
        if random_no <= 50:
            self.current_location = 'room'
            self.current_event = self.generate_room()
            return self.get_current_scene()
        elif random_no <= 75:
            self.current_location = 'shop'
            self.current_event = self.generate_shop()
            return self.get_current_scene()
        elif random_no <= 85:
            self.current_location = 'event'
            self.current_event = self.generate_random_event()
            return self.get_current_scene()
        else:
            self.game.messages.append("You walk and walk and nothing interesting happens")
            return {
                'choices': ["Continue traveling"]
            }

    def generate_shop(self):
        name_list = ["Zossy's Sharpies", "Bran's Boom-Booms", "Mesmash Things", "Swords Galore", "Pick'a'Sord", "Weaponsbury", "Bear Sword"]
        name = random.choice(name_list)
        return Shop(name, self.game)

    def generate_room(self):
        return Room(self.player, self.game)

    def generate_random_event(self):
        random_no = random.randint(0, 2)
        return RandomEvent(random_no, self.player, self.game)






