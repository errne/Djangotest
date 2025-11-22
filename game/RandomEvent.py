import random
from .Reputation import ReputationLevel
from .Quest import Quest


class RandomEvent:
    GUILD_GREETINGS = {
        ReputationLevel.UNKNOWN: [
            "Hello, stranger.",
            "I don’t believe we've met.",
        ],
        ReputationLevel.HATED: [
            "What do you want?",
            "Stay back. We haven't forgotten what you did.",
        ],
        ReputationLevel.DISLIKED: [
            "Oh… it's you.",
            "Make it quick.",
        ],
        ReputationLevel.NEUTRAL: [
            "Hello, there.",
            "Greetings, traveler.",
            "Good day, adventurer.",
        ],
        ReputationLevel.LIKED: [
            "Ah, good to see you again!",
            "Welcome back, friend.",
            "Your presence is always appreciated.",
        ],
        ReputationLevel.FRIENDLY: [
            "Our brightest mind returns!",
            "Always a pleasure to welcome you!",
            "You honor the guild with your visit.",
        ],
    }

    def __init__(self, seed, player, game):
        self.seed = seed
        self.player = player
        self.game = game
        self.question = None
        self.correct_answer = None

    def event_greeting(self):
        rep = self.player.get_reputation("Mathematicians Guild")
        options = self.GUILD_GREETINGS[rep]
        index = self.seed % len(options)
        return options[index]

    def event_task(self):
        questionno1 = random.randint(5, 13)
        questionno2 = random.randint(5, 13)
        self.question = f"what is {questionno1} times {questionno2}?"
        self.correct_answer = questionno1 * questionno2
        self.game.messages.append(self.question)
        return {
            'choices': self.get_choices()
        }

    def get_choices(self):
        return [str(self.correct_answer), str(self.correct_answer + random.randint(1, 5)), str(self.correct_answer - random.randint(1, 5))]

    def check_answer(self, answer):
        if int(answer) == self.correct_answer:
            self.player.add_gold_to_pouch(25)
            self.player.change_reputation("Mathematicians Guild", 3)
            self.game.messages.append("Correct. Your wisdom deserves some gold. 25 gold coins were added to your pouch")
        else:
            self.player.change_reputation("Mathematicians Guild", -1)
            self.game.messages.append("Incorrect, bye")
            self.player.change_reputation("Mathematicians Guild", -1)
            self.game.messages.append("Incorrect, bye")

class QuestEvent:
    def __init__(self, player, game):
        self.player = player
        self.game = game
        self.choices = ["Accept Quest", "Decline"]

    def event_greeting(self):
        return "A distraught villager approaches you."

    def event_task(self):
        self.game.messages.append("Please, help me! Thieves stole my family heirloom. Can you retrieve it?")
        return {
            'choices': self.choices
        }
    
    def get_choices(self):
        return self.choices

    def check_answer(self, choice):
        if choice == "Accept Quest":
            quest = Quest("Retrieve Heirloom", "Retrieve the stolen family heirloom from the Thieves Den.", reward_gold=100)
            self.player.add_quest(quest)
            self.game.messages.append("You accepted the quest!")
        else:
            self.game.messages.append("You walked away.")
