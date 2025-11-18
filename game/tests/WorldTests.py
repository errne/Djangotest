import unittest

from game.Player import Player
from game.RandomEvent import *
from game.World import *


class MockGame:
    def __init__(self):
        self.messages = []

class WorldTests(unittest.TestCase):

    def setUp(self):
        self.game = MockGame()
        self.player = Player("Obi", self.game)
        self.world = World(self.player, self.game) # Passing None for game object as it is not used in this test
        self.event = RandomEvent(1, self.player, self.game)

    def test_random_event_greeting(self):
        new_event = self.world.generate_random_event()
        greetings = ["Hello, there", "Greetings, traveler", "Good day, adventurer"]
        self.assertTrue(new_event.event_greeting() in greetings)
