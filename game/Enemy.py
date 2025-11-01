import random


class Enemy:
    max_hp = 75
    is_alive = True
    types = ["Undead", "Humanoid", "Animal"]
    names_for_undead = ["Zombie", "Vampire", "Forsaken", "Skeleton"]
    names_for_animals = ["Cave Bear", "Cave Wolf", "Lizard", "Giant Bat"]
    names_for_humanoids = ["Warrior", "Bandit", "Warlock", "Assassin"]
    all_names = [names_for_undead, names_for_humanoids, names_for_animals]

    def __init__(self):
        self.random_for_type = random.randint(0, len(self.types) - 1)
        self.random_for_name = random.randint(0, 3)
        self.type = self.types[self.random_for_type]
        self.name = self.all_names[self.random_for_type][self.random_for_name]
        self.hp = random.randint(10, self.max_hp)
        self.max_attack_damage = 25
        # self.attackDamage = random.randint(3, 25)
        self.armour = self.pick_armour_level()

    def hp_count(self):
        return self.hp

    def pick_armour_level(self):
        if self.random_for_type == 0:
            return 3
        elif self.random_for_type == 1:
            return 4
        else:
            return 2

    def deal_damage_to_player(self):
        return random.randint(3, self.max_attack_damage)

    def receive_damage(self, received_damage):
        received_damage_with_armour = received_damage - self.armour
        damage_received = max(0, received_damage_with_armour)
        self.hp -= damage_received
        if self.hp < 1:
            self.is_alive = False
            self.hp = 0

    def to_string(self):
        return f"You meet a {self.name} who has {self.hp} hp and wants to fight you"
