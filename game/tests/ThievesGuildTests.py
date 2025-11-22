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
        quest = Quest("test_quest", "Test Quest", "Description", reward_gold=50)
        self.assertEqual(quest.name, "Test Quest")
        self.assertFalse(quest.is_completed)
        
        quest.complete()
        self.assertTrue(quest.is_completed)

    def test_player_quest_management(self):
        quest = Quest("test_quest", "Test Quest", "Description", reward_gold=50)
        self.player.add_quest(quest)
        self.assertTrue(self.player.has_quest("test_quest"))
        
        initial_gold = self.player.gold_pouch
        self.player.complete_quest("test_quest")
        
        self.assertFalse(self.player.has_quest("test_quest")) # Should be false because it's completed
        self.assertTrue(quest.is_completed)
        self.assertEqual(self.player.gold_pouch, initial_gold + 50)

    def test_thieves_den_loot(self):
        den = ThievesDen(self.player, self.game)
        quest = Quest("retrieve_heirloom", "Retrieve Heirloom", "Description", reward_gold=100)
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
        self.assertTrue(self.player.has_quest("retrieve_heirloom"))
        self.assertIn("You accepted the quest!", self.game.messages)

    def test_reputation_loss(self):
        thief = ThiefEnemy()
        initial_rep = self.player.reputation["Thieves Guild"] or 0
        thief.on_death(self.player)
        
        new_rep = self.player.reputation["Thieves Guild"]
        self.assertEqual(new_rep, initial_rep - 10)
        self.assertIn("Your reputation with the Thieves Guild has decreased.", self.game.messages)

    def test_quests_view(self):
        # Setup session
        import pickle
        import base64
        from game.World import World
        
        # Create a request object (mocking it)
        class MockRequest:
            def __init__(self, session):
                self.session = session
                self.method = 'GET'
        
        world = World(self.player, self.game)
        game_state = {
            'world': base64.b64encode(pickle.dumps(world)).decode('utf-8')
        }
        request = MockRequest({'game_state': game_state})
        
        # Add a quest
        quest = Quest("test_quest", "Test Quest", "Description", reward_gold=50)
        self.player.add_quest(quest)
        
        # We need to update the world in the session because the view loads it from there
        # But here we are testing the view logic, which loads from session.
        # So we need to make sure the session has the updated player.
        world.player = self.player
        request.session['game_state']['world'] = base64.b64encode(pickle.dumps(world)).decode('utf-8')

        from unittest.mock import patch, MagicMock
        import sys
        
        # Mock django modules to avoid ModuleNotFoundError
        sys.modules['django'] = MagicMock()
        sys.modules['django.shortcuts'] = MagicMock()
        
        with patch('game.views.render') as mock_render:
            # We need to reload game.views if it was already imported, or just import it
            # But since it failed before, it probably wasn't imported successfully.
            # However, if we mock sys.modules, we need to make sure we don't break other tests if they needed real django (unlikely here).
            
            from game.views import quests_view
            quests_view(request)
            
            # Verify render was called
            # Note: since we mocked django.shortcuts, game.views.render IS the mock from sys.modules['django.shortcuts'].render
            # But we also patched 'game.views.render'.
            # Let's see which one wins. Patching 'game.views.render' should work if game.views exists.
            # But game.views import will use the mocked django.shortcuts.
            # So game.views.render will be the MagicMock from sys.modules.
            # We should probably just use that mock.
            
            # Actually, if we patch 'game.views.render', unittest.mock handles the lookup.
            # But we need to make sure game.views can be imported first.
            
            self.assertTrue(mock_render.called)
            args, kwargs = mock_render.call_args
            
            # Check template name
            self.assertEqual(args[1], 'game/quests.html')
            
            # Check context
            context = args[2]
            self.assertEqual(context['character_name'], "TestPlayer")
            self.assertEqual(len(context['active_quests']), 1)
            self.assertEqual(context['active_quests'][0].name, "Test Quest")
            self.assertEqual(len(context['completed_quests']), 0)



    def test_quest_repeatability(self):
        from game.World import World
        from game.RandomEvent import QuestEvent, RandomEvent
        from unittest.mock import patch
        
        world = World(self.player, self.game)
        
        # 1. Complete the quest once
        quest = Quest("retrieve_heirloom", "Retrieve Heirloom", "Description", reward_gold=100)
        quest.complete()
        self.player.add_quest(quest)
        
        # 2. Try to generate random event
        # We need to mock random to ensure we hit the 30% chance IF the condition passes
        # The condition is: if not has_quest and not any(completed)
        # We want to verify that 'not any(completed)' blocks it.
        
        with patch('random.randint') as mock_randint:
            # Force the 30% check to pass (return 1)
            mock_randint.return_value = 1
            
            event = world.generate_random_event()
            
            # If blocked, it returns RandomEvent (because condition failed)
            # If not blocked, it returns QuestEvent
            
            # If blocked, it returns RandomEvent (because condition failed)
            # If not blocked, it returns QuestEvent
            
            # Now it SHOULD NOT be blocked, so we expect QuestEvent
            self.assertIsInstance(event, QuestEvent)

    def test_inventory_limit(self):
        from game.Weapon import Weapon
        from game.MaterialTypes import MaterialTypes
        from game.WeaponTypes import WeaponTypes
        
        # 1. Fill inventory
        # Limit is 24
        for i in range(24):
            weapon = Weapon(MaterialTypes.WOOD, WeaponTypes.SWORD)
            success = self.player.add_item_to_inventory(weapon)
            self.assertTrue(success, f"Failed to add item {i+1}")
            
        self.assertEqual(len(self.player.inventory), 24)
        
        # 2. Try to add 25th item
        weapon = Weapon(MaterialTypes.WOOD, WeaponTypes.SWORD)
        success = self.player.add_item_to_inventory(weapon)
        self.assertFalse(success, "Should not be able to add 25th item")
        self.assertEqual(len(self.player.inventory), 24)
        self.assertIn("Inventory full!", self.game.messages)
        
        # 3. Try to buy item from shop (requires unequip old weapon -> needs space)
        # Player starts with a weapon equipped.
        # Buying a new weapon means: old weapon -> inventory.
        # Inventory is full (24).
        # So buying should fail.
        
        from game.Shop import Shop
        shop = Shop("Test Shop", self.game)
        # Give player gold
        self.player.gold_pouch = 1000
        
        # Shop generates weapons. Let's buy the first one.
        # Shop.buy_item(player, index)
        
        # Clear messages
        self.game.messages.clear()
        
        shop.buy_item(self.player, 0)
        
        # Should fail
        self.assertIn("Inventory full! Cannot unequip current weapon.", self.game.messages)
        # Gold should not decrease (price is max_damage * 3, approx 30-100)
        self.assertEqual(self.player.gold_pouch, 1000)

if __name__ == '__main__':
    unittest.main()

