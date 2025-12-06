"""
Lost but Found - Main Entry Point
"""

import sys
from game.game_manager import GameManager

def main():
    # instantiate GameManager
    game = GameManager()
    # run the game
    game.run()
    # exit
    sys.exit()

if __name__ == "__main__":
    main()