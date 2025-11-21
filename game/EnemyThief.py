import random
from .Enemy import Enemy

class ThiefEnemy(Enemy):
    thief_names = ["Cutpurse", "Footpad", "Shadowblade", "Guild Enforcer"]

    def __init__(self):
        super().__init__()
        self.type = "Humanoid"
        self.name = random.choice(self.thief_names)
        self.max_attack_damage = 18
        self.hp = random.randint(20, 60)
        # self.faction = Faction.THIEVES_GUILD maybe add factions
        self.armour = 3

    def to_string(self):
        return f"You meet a {self.name} who has {self.hp} hp and they attack you on sight"

    # unused as of yet
    def specific_drops(self):
        return ["Stolen Purse", "Lockpick", "Guild Token"]

    def on_death(self, player):
        player.change_reputation("Thieves Guild", -10)
        # We can't access game.messages directly here easily without passing game or having it on player/enemy
        # But player has game reference usually? Let's check Player.py
        # Player has self.game. So we can use player.game.messages
        player.game.messages.append("Your reputation with the Thieves Guild has decreased.")
