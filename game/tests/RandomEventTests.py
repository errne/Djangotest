import unittest

from game.Player import Player
from game.RandomEvent import *


class RandomEventTests(unittest.TestCase):

    def setUp(self):
        self.player = Player("Obi", None)
        self.event = RandomEvent(1, self.player, None)

    def test_event_greeting(self):
        self.assertEqual("Greetings, traveler", self.event.event_greeting())
        self.assertNotEqual("Heloooo,", self.event.event_greeting())

