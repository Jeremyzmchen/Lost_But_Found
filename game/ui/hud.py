"""
游戏HUD（Heads-Up Display）- 显示游戏信息 (倒计时修正版)
"""

import pygame
from config.settings import *

class HUD:
    """游戏HUD - 显示金钱、时间等信息"""

    def __init__(self):
        """初始化HUD"""
        # 加载字体
        try:
            self.font_large = pygame.font.Font(FONT_PATH, 48)
            self.font_medium = pygame.font.Font(FONT_PATH, 36)
            self.font_small = pygame.font.Font(FONT_PATH, 28)
        except:
            self.font_large = pygame.font.Font(None, 48)
            self.font_medium = pygame.font.Font(None, 36)
            self.font_small = pygame.font.Font(None, 28)

    def _format_time(self, seconds):
        """格式化时间显示 MM:SS"""
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02d}:{secs:02d}"

    def render(self, screen, money, shift_time, shift_duration):
        """
        渲染HUD
        Args:
            shift_time: 已工作时间
            shift_duration: 班次总时长
        """
        # --- 1. 右上角 - 金钱显示 ---
        money_text = self.font_large.render(f"${money}", True, COLOR_GREEN)
        money_rect = money_text.get_rect(topright=(WINDOW_WIDTH - 20, 20))

        # 绘制金钱背景
        bg_rect = money_rect.inflate(20, 10)
        pygame.draw.rect(screen, COLOR_BLACK, bg_rect, border_radius=5)
        pygame.draw.rect(screen, COLOR_WHITE, bg_rect, 2, border_radius=5)
        screen.blit(money_text, money_rect)

        # --- 2. 右下角 - 倒计时显示 [修改重点] ---

        # 计算剩余时间
        time_left = max(0, int(shift_duration - shift_time))

        # 颜色逻辑：最后30秒变红
        if time_left <= 30:
            time_color = COLOR_RED
        else:
            time_color = COLOR_WHITE

        time_text = self.font_medium.render(
            self._format_time(time_left), # 显示剩余时间
            True,
            time_color
        )
        time_rect = time_text.get_rect(bottomright=(WINDOW_WIDTH - 20, WINDOW_HEIGHT - 20))

        time_bg = time_rect.inflate(20, 10)
        pygame.draw.rect(screen, COLOR_BLACK, time_bg, border_radius=5)
        pygame.draw.rect(screen, time_color, time_bg, 2, border_radius=5) # 边框颜色也跟着变
        screen.blit(time_text, time_rect)

