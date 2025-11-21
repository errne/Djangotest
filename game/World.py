import random
from .RandomEvent import RandomEvent, QuestEvent
from .Room import Room
from .ThievesDen import ThievesDen
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
            if self.player.has_quest("Retrieve Heirloom"):
                # 50% chance to find the den if quest is active
                if random.randint(0, 1) == 0:
                    room_event = ThievesDen(self.player, self.game)
                else:
                    room_event = self.generate_room()
            else:
                room_event = self.generate_room()
            
            self.current_state = RoomState(self, room_event)
            return self.get_current_scene()
        elif random_no <= 55:
            shop_event = self.generate_shop()
            self.current_state = ShopState(self, shop_event)
            return self.get_current_scene()
        elif random_no <= 95:
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
        # Check if we should spawn the quest event
        if not self.player.has_quest("Retrieve Heirloom") and not any(q.name == "Retrieve Heirloom" and q.is_completed for q in self.player.quests):
             # 30% chance to get the quest if not already active/completed
             if random.randint(1, 100) <= 30:
                 return QuestEvent(self.player, self.game)

        random_no = random.randint(0, 2)
        return RandomEvent(random_no, self.player, self.game)






