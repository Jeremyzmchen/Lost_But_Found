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

        # [修改] 移除了 Restart 按钮，只保留 Main Menu 和 Quit

        # 1. 回到主菜单
        self.btn_menu = Button(center_x - 120, start_y, 240, 60, "MAIN MENU", self._to_main_menu)

        # 2. 退出游戏
        self.btn_quit = Button(center_x - 120, start_y + spacing, 240, 60, "QUIT", self._quit_game)

    def _load_background(self):
        try:
            bg_path = ASSETS.get('bg_menu')
            if bg_path:
                self.background = pygame.image.load(bg_path)
                self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))
                dark = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
                dark.fill((0, 0, 0))
                dark.set_alpha(180)
                self.background.blit(dark, (0,0))
        except:
            self.background = None

    def _to_main_menu(self):
        """回到主菜单"""
        from game.game_manager import GameState
        self.game_manager.change_state(GameState.MENU)

    def _quit_game(self):
        """退出程序"""
        pygame.quit()
        sys.exit()

    """
    GameOverState 是在游戏刚启动时（__init__ 里）就被创建出来的。
    这意味着 GameOverState 的 __init__ 只会在程序启动时运行一次。
    此时，你的 self.money 是 0。
    数据需要刷新： 当你玩完第一局，赚了 $500，游戏切换到结算界面。
    如果有 enter：系统会告诉结算界面：“嘿，这局赚了 $500，快更新显示！” -> 界面显示 $500。
    如果没有 enter：结算界面还是维持着初始化时的状态 -> 界面永远显示 $0。
    """
    def enter(self, **kwargs):
        if 'money' in kwargs: self.money = kwargs['money']
        if 'difficulty' in kwargs: self.difficulty = kwargs['difficulty']

    def exit(self):
        pass

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

        title = self.font_title.render("SHIFT COMPLETE", True, COLOR_GREEN)
        title_rect = title.get_rect(center=(center_x, 180))
        screen.blit(title, title_rect)

        score_txt = self.font_title.render(f"${self.money}", True, COLOR_YELLOW)
        score_rect = score_txt.get_rect(center=(center_x, 330))
        screen.blit(score_txt, score_rect)

        # [修改] 只渲染剩下的两个按钮
        self.btn_menu.render(screen)
        self.btn_quit.render(screen)