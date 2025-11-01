import random

class RandomEvent:
    greetings = ["Hello, there", "Greetings, traveler", "Good day, adventurer"]

    def __init__(self, seed, player):
        self.seed = seed
        self.player = player
        self.question = None
        self.correct_answer = None

    def event_greeting(self):
        return self.greetings[self.seed]

    def event_task(self):
        questionno1 = random.randint(5, 13)
        questionno2 = random.randint(5, 13)
        self.question = f"what is {questionno1} times {questionno2}?"
        self.correct_answer = questionno1 * questionno2
        return {
            'text': self.question,
            'choices': self.get_choices()
        }

    def get_choices(self):
        # In a real game, you'd generate more believable wrong answers
        return [str(self.correct_answer), str(self.correct_answer + random.randint(1, 5)), str(self.correct_answer - random.randint(1, 5))]

    def check_answer(self, answer):
        if int(answer) == self.correct_answer:
            self.player.add_gold_to_pouch(25)
            return "Correct. Your wisdom deserves some gold. 25 gold coins were added to your pouch"
        else:
            return "Incorrect, bye"
