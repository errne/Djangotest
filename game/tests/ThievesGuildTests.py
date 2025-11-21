import unittest
from game.EnemyThief import ThiefEnemy
from game.Quest import Quest
from game.Player import Player
from game.ThievesDen import ThievesDen
from game.RandomEvent import QuestEvent
from game.Game import Game

class ThievesGuildTests(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.player = Player("TestPlayer", self.game)

    def test_thief_enemy(self):
        thief = ThiefEnemy()
        self.assertEqual(thief.type, "Humanoid")
        self.assertIn(thief.name, ThiefEnemy.thief_names)
        self.assertTrue(20 <= thief.hp <= 60)
        self.assertEqual(thief.armour, 3)

    def test_quest_creation_and_completion(self):
        quest = Quest("Test Quest", "Description", reward_gold=50)
        self.assertEqual(quest.name, "Test Quest")
        self.assertFalse(quest.is_completed)
        
        quest.complete()
        self.assertTrue(quest.is_completed)

    def test_player_quest_management(self):
        quest = Quest("Test Quest", "Description", reward_gold=50)
        self.player.add_quest(quest)
        self.assertTrue(self.player.has_quest("Test Quest"))
        
        initial_gold = self.player.gold_pouch
        self.player.complete_quest("Test Quest")
        
        self.assertFalse(self.player.has_quest("Test Quest")) # Should be false because it's completed
        self.assertTrue(quest.is_completed)
        self.assertEqual(self.player.gold_pouch, initial_gold + 50)

    def test_thieves_den_loot(self):
        den = ThievesDen(self.player, self.game)
        quest = Quest("Retrieve Heirloom", "Description", reward_gold=100)
        self.player.add_quest(quest)
        
        # Simulate clearing the room
        den.loot_treasure_chest()
        
        self.assertTrue(quest.is_completed)
        self.assertIn("You found the Stolen Heirloom in the chest!", self.game.messages)

    def test_quest_event(self):
        event = QuestEvent(self.player, self.game)
        choices = event.get_choices()
        self.assertIn("Accept Quest", choices)
        
        event.check_answer("Accept Quest")
        self.assertTrue(self.player.has_quest("Retrieve Heirloom"))
        self.assertIn("You accepted the quest!", self.game.messages)

    def test_reputation_loss(self):
        thief = ThiefEnemy()
        initial_rep = self.player.reputation["Thieves Guild"] or 0
        thief.on_death(self.player)
        
        new_rep = self.player.reputation["Thieves Guild"]
        self.assertEqual(new_rep, initial_rep - 10)
        self.assertIn("Your reputation with the Thieves Guild has decreased.", self.game.messages)

if __name__ == '__main__':
    unittest.main()
