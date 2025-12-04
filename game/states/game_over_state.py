"""
游戏结算状态 - 单局结算版 (去除了 Restart 功能)
"""

import pygame
import sys
from config.settings import *
from game.ui.button import Button

class GameOverState:
    """结算状态"""

    def __init__(self, game_manager):
        self.game_manager = game_manager

        # 获取了 money 数据进行结算显示
        self.money = self.game_manager.game_data.get('money', 0)

        #加载了背景图片(_load_background) 和字体
        self.font_title = pygame.font.Font(FONT_PATH, 80)
        self.font_text = pygame.font.Font(FONT_PATH, 40)
        self.background = None
        self._load_background()
        center_x = WINDOW_WIDTH // 2
        start_y = 500
        spacing = 80

        # 1. 回到主菜单
        self.btn_menu = Button(center_x - 120, start_y, 240, 60, "MAIN MENU", self._to_main_menu)

        # 2. 退出游戏
        self.btn_quit = Button(center_x - 120, start_y + spacing, 240, 60, "QUIT", self._quit_game)

    def _load_background(self):
        self.background = pygame.transform.scale(
            pygame.image.load(ASSETS['bg_game_over']),
            (WINDOW_WIDTH, WINDOW_HEIGHT)
        )

    def _to_main_menu(self):
        """回到主菜单"""
        from game.game_manager import GameState
        self.game_manager.change_state(GameState.MENU)

    def _quit_game(self):
        """退出程序"""
        pygame.quit()
        sys.exit()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            # [修改] 移除了 btn_restart 的检测
            self.btn_menu.handle_click(mouse_pos)
            self.btn_quit.handle_click(mouse_pos)

    def update(self, dt):
        mouse_pos = pygame.mouse.get_pos()
        # [修改] 移除了 btn_restart 的更新
        self.btn_menu.update(mouse_pos)
        self.btn_quit.update(mouse_pos)

    def render(self, screen):
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            screen.fill(COLOR_DARK_GRAY)

        center_x = WINDOW_WIDTH // 2

        title = self.font_title.render("GAME OVER", True, COLOR_WHITE)
        title_rect = title.get_rect(center=(center_x, 180))
        screen.blit(title, title_rect)

        score_txt = self.font_title.render(f"${self.money}", True, COLOR_YELLOW)
        score_rect = score_txt.get_rect(center=(center_x, 330))
        screen.blit(score_txt, score_rect)

        # [修改] 只渲染剩下的两个按钮
        self.btn_menu.render(screen)
        self.btn_quit.render(screen)