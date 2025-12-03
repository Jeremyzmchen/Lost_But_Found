"""
游戏管理器 - 负责状态切换和主循环
"""

import pygame
from enum import Enum  # [新增] 引入Enum

from config.settings import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, FPS

# [修改] 直接在这里定义 GameState，不需要从外部引入
class GameState(Enum):
    MENU = "menu"
    GAMEPLAY = "gameplay"
    GAME_OVER = "game_over"

# 引入所有状态类
# 注意：这里不再需要从 game.states 引入 GameState 了
from game.states.menu_state import MenuState
from game.states.gameplay_state import GameplayState
from game.states.game_over_state import GameOverState

class GameManager:
    """游戏总控类"""

    def __init__(self):
        # 初始化 Pygame
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

        # 全局数据
        self.game_data = {
            'money': 0,
            'difficulty': 'normal'
        }

        # 初始化所有状态
        self.states = {
            GameState.MENU: MenuState(self),
            GameState.GAMEPLAY: GameplayState(self),
            GameState.GAME_OVER: GameOverState(self)
        }

        # 初始状态
        self.current_state = GameState.MENU

    def change_state(self, new_state, **kwargs):
        """
        切换状态
        Args:
            new_state: GameState 枚举值 (例如 GameState.GAMEPLAY)
            **kwargs: 需要传递给新状态的数据
        """
        self.game_data.update(kwargs)
        self.current_state = new_state

        state_instance = self.states[self.current_state]
        if hasattr(state_instance, 'enter'):
            state_instance.enter(**kwargs)

        print(f"🔄 状态切换: {new_state}")

    def handle_event(self, event):
        self.states[self.current_state].handle_event(event)

    def update(self, dt):
        self.states[self.current_state].update(dt)

    def render(self):
        self.states[self.current_state].render(self.screen)

    def run(self):
        """主循环"""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.handle_event(event)

            self.update(dt)
            self.render()
            pygame.display.flip()

        pygame.quit()