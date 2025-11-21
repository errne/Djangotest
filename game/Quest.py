class Quest:
    def __init__(self, name, description, target_item=None, reward_gold=0, is_completed=False):
        self.name = name
        self.description = description
        self.target_item = target_item
        self.reward_gold = reward_gold
        self.is_completed = is_completed

    def complete(self):
        self.is_completed = True
