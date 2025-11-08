import random
from .RandomEvent import RandomEvent
from .Room import Room
from .Shop import Shop
from .world_states import RoadState, EquipState, ShopState, RoomState, ClearedRoomState, EventState # Import all state classes

class World:
    def __init__(self, player, game):
        self.player = player
        self.game = game
        self.current_state = RoadState(self) # Initialize with the starting state

    def get_current_scene(self):
        return self.current_state.get_scene()

    def handle_choice(self, choice_index):
        return self.current_state.handle_choice(choice_index)

    def generate_next_stop(self):
        random_no = random.randint(1, 100)
        if random_no <= 50:
            room_event = self.generate_room()
            self.current_state = RoomState(self, room_event)
            return self.get_current_scene()
        elif random_no <= 75:
            shop_event = self.generate_shop()
            self.current_state = ShopState(self, shop_event)
            return self.get_current_scene()
        elif random_no <= 85:
            random_event = self.generate_random_event()
            self.current_state = EventState(self, random_event)
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






