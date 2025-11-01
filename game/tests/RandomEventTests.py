import unittest

from Player import Player
from RandomEvent import *


class RandomEventTests(unittest.TestCase):

    def setUp(self):
        self.player = Player("Obi")
        self.event = RandomEvent(1, self.player)

    def test_event_greeting(self):
        self.assertEqual("Greetings, traveler", self.event.event_greeting())
        self.assertNotEqual("Heloooo,", self.event.event_greeting())

