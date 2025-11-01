import unittest

from Player import Player
from RandomEvent import *
from World import *


class WorldTests(unittest.TestCase):

    def setUp(self):
        self.player = Player("Obi")
        self.world = World(self.player, None) # Passing None for game object as it is not used in this test
        self.event = RandomEvent(1, self.player)

    def test_random_event_greeting(self):
        new_event = self.world.generate_random_event()
        greetings = ["Hello, there", "Greetings, traveler", "Good day, adventurer"]
        self.assertTrue(new_event.event_greeting() in greetings)
