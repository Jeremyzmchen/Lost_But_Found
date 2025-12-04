import pygame
import random
import os
from config.settings import *
from game.ui.button import Button

class Customer:
    """顾客类"""

    def __init__(self, sought_item_type, target_x=WINDOW_WIDTH//2): # [修改] 移除 difficulty
        self.sought_item_type = sought_item_type
        self.item_data = ITEM_DESCRIPTIONS.get(sought_item_type, {})

        self.description = self._generate_description()

        # [修改] 直接使用全局定义的等待时间
        self.max_wait_time = CUSTOMER_WAIT_TIME

        self.wait_time = 0
        self.patience = 1.0

        # 位置与运动
        self.x = target_x
        self.y = -100
        self.target_y = CUSTOMER_Y
        self.speed = 400

        self.state = 'walking_in'

        # 资源加载
        self.image = None
        self.bubble_image = None
        self._load_resources()

        self.dialog_visible = False

        self.font = pygame.font.Font(FONT_PATH, 24)
        self.font_small = pygame.font.Font(FONT_PATH, 20)

        self.reject_button = Button(0, 0, 150, 35, "Don't Have", None, style='grey', font_size=24)

    @property
    def is_arrived(self):
        return self.state == 'waiting'

    def get_delivery_rect(self):
        return pygame.Rect(self.x - 100, self.y - 100, 200, 250)

    def _generate_description(self):
        keywords = self.item_data.get('keywords', [])
        if not keywords: return "I lost something..."
        num_keywords = random.randint(1, min(3, len(keywords)))
        selected_keywords = random.sample(keywords, num_keywords)
        descriptions = [
            f"I lost my {selected_keywords[0]}",
            f"Looking for {', '.join(selected_keywords[:2])}",
            f"Seen my {selected_keywords[0]}?",
            f"My {self.item_data.get('name', 'item')} missing",
        ]
        return random.choice(descriptions)

    def _load_resources(self):
        try:
            customer_images = [
                'npc_1', 'npc_2', 'npc_3', 'npc_4',
                'npc_5', 'npc_6', 'npc_7', 'npc_8',
                'npc_9', 'npc_10', 'npc_11', 'npc_12']
            image_key = random.choice(customer_images)
            if image_key in ASSETS:
                self.image = pygame.image.load(ASSETS[image_key])
                self.image = pygame.transform.scale(self.image, (375, 470))
        except: pass

        if not self.image:
            self.image = pygame.Surface((100, 100))
            self.image.fill((150, 150, 200))
            pygame.draw.circle(self.image, (255, 200, 150), (50, 50), 40)

        try:
            bubble_path = 'assets/images/icons/bubble_box.png'
            if os.path.exists(bubble_path):
                self.bubble_image = pygame.image.load(bubble_path)
        except: pass

    def update(self, dt):
        if self.state == 'walking_in':
            self.y += self.speed * dt
            if self.y >= self.target_y:
                self.y = self.target_y
                self.state = 'waiting'
                self.dialog_visible = True

        elif self.state == 'waiting':
            self.wait_time += dt
            self.patience = max(0, 1.0 - (self.wait_time / self.max_wait_time))

            # 气泡底部Y = 顾客头顶Y + 气泡高度
            dialog_height = 120
            bubble_bottom_y = 200 + dialog_height

            # 按钮居中：顾客X - 按钮宽的一半
            btn_x = self.x - self.reject_button.rect.width // 2
            # 按钮位置：气泡底部 + 5像素间距
            btn_y = bubble_bottom_y + 5

            self.reject_button.rect.topleft = (btn_x, btn_y)
            self.reject_button.update(pygame.mouse.get_pos())

    def is_timeout(self):
        return self.wait_time >= self.max_wait_time

    def check_item_match(self, item):
        return item.item_type == self.sought_item_type

    def get_patience_color(self):
        if self.patience > 0.6: return COLOR_BLUE
        elif self.patience > 0.3: return COLOR_ORANGE
        else: return COLOR_RED

    def render(self, screen):
        if self.image:
            image_rect = self.image.get_rect(center=(self.x, self.y))
            screen.blit(self.image, image_rect)

        if self.dialog_visible:
            dialog_width = 268
            dialog_height = 135
            dialog_x = self.x - dialog_width // 2
            dialog_y = 205

            if self.bubble_image:
                bubble_scaled = pygame.transform.scale(self.bubble_image, (dialog_width, dialog_height))
                screen.blit(bubble_scaled, (dialog_x, dialog_y))
            else:
                pygame.draw.rect(screen, COLOR_WHITE, (dialog_x, dialog_y, dialog_width, dialog_height), border_radius=10)
                pygame.draw.rect(screen, COLOR_BLACK, (dialog_x, dialog_y, dialog_width, dialog_height), 2, border_radius=10)

            lines = self._wrap_text(self.description, self.font, dialog_width - 30)
            line_height = 25
            total_text_height = len(lines) * line_height
            content_area_height = dialog_height - 30
            text_start_y = dialog_y + (content_area_height - total_text_height) // 2 + 5

            for i, line in enumerate(lines):
                text = self.font.render(line, True, COLOR_BLACK)
                text_rect = text.get_rect(centerx=dialog_x + dialog_width//2, top=text_start_y + i * line_height)
                screen.blit(text, text_rect)

            bar_w = dialog_width - 100
            bar_x = dialog_x + 45
            bar_y = dialog_y + dialog_height - 35

            pygame.draw.rect(screen, COLOR_DARK_GRAY, (bar_x, bar_y, bar_w, 10), border_radius=4)
            fill = int(bar_w * self.patience)
            if fill > 0:
                pygame.draw.rect(screen, self.get_patience_color(), (bar_x, bar_y, fill, 10), border_radius=4)

            self.reject_button.render(screen)

    def _wrap_text(self, text, font, max_width):
        words = text.split(' ')
        lines = []
        current_line = []
        for word in words:
            test_line = ' '.join(current_line + [word])
            if font.size(test_line)[0] <= max_width:
                current_line.append(word)
            else:
                if current_line: lines.append(' '.join(current_line))
                current_line = [word]
        if current_line: lines.append(' '.join(current_line))
        return lines if lines else [text]