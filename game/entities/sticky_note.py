import pygame
import random
from game.entities.item import Item
from config.settings import COLOR_BLACK


class StickyNote(Item):
    """便签条 - 携带案件信息的特殊物品"""

    def __init__(self, x, y, sought_item_type):
        self.item_type = 'sticky_note'
        self.name = "Case Note"
        self.keywords = ['note', 'clue', 'paper']

        # 核心数据：原本顾客想要什么
        self.sought_item_type = sought_item_type

        # 随机生成 4 位案件编号 (用于显示和剧情)
        self.case_id = str(random.randint(1000, 9999))

        self.width = 70
        self.height = 80
        self.x = x
        self.y = y

        # 物理属性 (轻飘飘的纸张)
        self.friction = 0.85
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(2, 4)
        self.va = random.uniform(-5, 5)
        self.angle = random.uniform(-10, 10)

        # 状态
        self.is_selected = False
        self.in_storage = False
        self.on_conveyor = False
        self.batch_id = -1
        self.item_index = -1
        self.conveyor_start_offset = 0
        self.conveyor_vertical_offset = 0

        self._generate_image()
        self.rect = self.image.get_rect(center=(x, y))

    def _generate_image(self):
        # 1. 黄色背景
        self.original_image = pygame.Surface((self.width, self.height))
        self.original_image.fill((255, 240, 150))

        # 2. 红色 "CASE" 印章
        font_small = pygame.font.SysFont("arial", 14, bold=True)
        pygame.draw.rect(self.original_image, (200, 50, 50), (5, 5, 40, 20))
        lbl = font_small.render("CASE", True, (255, 255, 255))
        self.original_image.blit(lbl, (8, 6))

        # 3. 绘制 4 位数字 ID
        font_big = pygame.font.SysFont("arial", 26, bold=True)
        text = font_big.render(self.case_id, True, COLOR_BLACK)
        text_rect = text.get_rect(center=(self.width // 2, self.height // 2 + 5))
        self.original_image.blit(text, text_rect)

        # 4. 生成最终旋转图
        self.image = self.original_image.copy()
        self.image = pygame.transform.rotate(self.original_image, self.angle)