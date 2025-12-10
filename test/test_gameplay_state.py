import unittest
import sys
import os
from unittest.mock import MagicMock

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

# Mock Pygame
mock_pygame = MagicMock()
sys.modules['pygame'] = mock_pygame
sys.modules['pygame.mixer'] = mock_pygame.mixer
sys.modules['pygame.image'] = mock_pygame.image
sys.modules['pygame.font'] = mock_pygame.font
sys.modules['pygame.mouse'] = mock_pygame.mouse

try:
    from game.states.gameplay_state import GameplayState
except ImportError:
    from game.states.gameplay_state import GameplayState

class TestGameplayState(unittest.TestCase):

    def setUp(self):
        """init env"""
        self.mock_game_manager = MagicMock()
        self.game = GameplayState(self.mock_game_manager)

        self.game.sfx_money = MagicMock()
        self.game.sfx_deny = MagicMock()
        self.game._remove_customer = MagicMock()

        self.game.money = 0

    def test_delivery_correct_item(self):
        """test 1: delivery -> money + sound effect"""
        print("\ntesting: npc is receiving the right thing...")

        customer = MagicMock()
        customer.check_item_match.return_value = True
        item = MagicMock()
        self.game._handle_delivery(customer, item)

        self.assertGreater(self.game.money, 0, "error：money action lacked")

        self.game.sfx_money.play.assert_called_once()
        print("Pass: success")

    def test_delivery_wrong_item(self):
        """test 2: wrong delivery -> money + sound effect"""
        print("\ntesting: npc is receiving the wrong thing...")

        customer = MagicMock()
        customer.check_item_match.return_value = False

        item = MagicMock()
        self.game._handle_delivery(customer, item)

        self.assertLess(self.game.money, 0, "error：money action lacked")
        self.game.sfx_deny.play.assert_called_once()

        print("Pass: success")

if __name__ == '__main__':
    unittest.main()