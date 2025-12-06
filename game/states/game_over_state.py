"""
Game settlement status: data, button, img, music
"""

import pygame
import sys
from config.settings import *
from game.ui.button import Button

class GameOverState:
    def __init__(self, game_manager):
        self.game_manager = game_manager

        # Get player revenue data
        self.money = self.game_manager.game_data.get('money', 0)

        # Initialize fonts and img
        self.font_title = pygame.font.Font(FONT_PATH, 80)
        self.font_text = pygame.font.Font(FONT_PATH, 40)
        self.background = None
        self._load_background()
        start_x = WINDOW_WIDTH // 2
        start_y = 500
        spacing = 80

        # Initialize buttons
        self.btn_menu = Button(start_x - 120, start_y, 240, 60, "MAIN MENU", self._to_main_menu)
        self.btn_quit = Button(start_x - 120, start_y + spacing, 240, 60, "QUIT", self._quit_game)

    def _load_background(self):
        """Load background"""
        self.background = pygame.transform.scale(
            pygame.image.load(ASSETS['bg_game_over']),
            (WINDOW_WIDTH, WINDOW_HEIGHT)
        )

    def _to_main_menu(self):
        """Back to menu"""
        from game.game_manager import GameState
        self.game_manager.change_state(GameState.MENU)

    def _quit_game(self):
        """Quit"""
        pygame.quit()
        sys.exit()

    def handle_event(self, event):
        """Handle mouse event"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            self.btn_menu.handle_click(mouse_pos)
            self.btn_quit.handle_click(mouse_pos)

    def update(self, dt):
        """Update mouse event"""
        mouse_pos = pygame.mouse.get_pos()
        self.btn_menu.update(mouse_pos)
        self.btn_quit.update(mouse_pos)

    def render(self, screen):
        """Render"""
        # 1. render background
        if self.background: screen.blit(self.background, (0, 0))
        else: screen.fill(COLOR_DARK_GRAY)

        # 2. Render title
        center_x = WINDOW_WIDTH // 2
        title = self.font_title.render("GAME OVER", True, COLOR_WHITE)
        title_rect = title.get_rect(center=(center_x, 180))
        screen.blit(title, title_rect)

        # 3. Render data
        score_txt = self.font_title.render(f"${self.money}", True, COLOR_YELLOW)
        score_rect = score_txt.get_rect(center=(center_x, 330))
        screen.blit(score_txt, score_rect)

        # 4. Render buttons
        self.btn_menu.render(screen)
        self.btn_quit.render(screen)