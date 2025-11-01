import random
from .RandomEvent import RandomEvent
from .Room import Room
from .Shop import Shop

class World:
    def __init__(self, player, game):
        self.player = player
        self.game = game
        self.current_location = None  # Can be 'room', 'shop', 'event', or None
        self.current_event = None

    def get_current_scene(self):
        if self.current_location is None:
            return {
                'text': "You are on the road.",
                'choices': ["Continue traveling", "Check inventory", "Save and quit"]
            }
        elif self.current_location == 'shop':
            shop = self.current_event
            return shop.get_shop_menu()
        elif self.current_location == 'room':
            room = self.current_event
            return room.handle_combat_turn(None) # Get initial combat scene
        elif self.current_location == 'event':
            event = self.current_event
            return event.event_task()

    def handle_choice(self, choice_index):
        if self.current_location is None:
            if choice_index == 0:  # Continue traveling
                return self.generate_next_stop()
            elif choice_index == 1:  # Check inventory
                return {'text': self.player.check_inventory(), 'choices': ["Back to road"]}
            elif choice_index == 2:  # Save and quit
                self.game.save_game(self.player)
                return {'text': "Game saved. Thanks for playing!", 'choices': []}
        elif self.current_location == 'shop':
            shop = self.current_event
            # This is a simplified logic, you might need to handle sub-menus
            if choice_index == 0: # Buy
                return shop.get_buy_menu()
            elif choice_index == 1: # Sell
                return shop.get_sell_menu(self.player)
            else: # Leave
                self.current_location = None
                return self.get_current_scene()
        elif self.current_location == 'room':
            room = self.current_event
            choice = room.handle_combat_turn(None)['choices'][choice_index]
            scene = room.handle_combat_turn(choice)
            if scene['choices'] == ["Leave room"]:
                self.current_location = None
            return scene
        elif self.current_location == 'event':
            event = self.current_event
            choice = event.get_choices()[choice_index]
            result = event.check_answer(choice)
            self.current_location = None
            return {'text': result, 'choices': ["Continue traveling"]}

    def generate_next_stop(self):
        random_no = random.randint(1, 100)
        if random_no <= 50:
            self.current_location = 'room'
            self.current_event = self.generate_room()
            return self.get_current_scene()
        elif random_no <= 65:
            self.current_location = 'shop'
            self.current_event = self.generate_shop()
            return self.get_current_scene()
        elif random_no <= 85:
            self.current_location = 'event'
            self.current_event = self.generate_random_event()
            return self.get_current_scene()
        else:
            return {
                'text': "You walk and walk and nothing interesting happens",
                'choices': ["Continue traveling"]
            }

    def generate_shop(self):
        name_list = ["Zossy's Sharpies", "Bran's Boom-Booms", "Mesmash Things", "Swords Galore", "Pick'a'Sord", "Weaponsbury"]
        name = random.choice(name_list)
        return Shop(name)

    def generate_room(self):
        return Room(self.player)

    def generate_random_event(self):
        random_no = random.randint(0, 2)
        return RandomEvent(random_no, self.player)






