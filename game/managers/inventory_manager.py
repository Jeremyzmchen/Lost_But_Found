"""
库存管理器 - 管理桌面上所有物品 (精简版：去除了储物柜逻辑)
"""

import pygame
import random
from config.settings import DESK_AREA

class InventoryManager:
    """库存管理器"""

    def __init__(self):
        # 只有一个列表：桌面物品
        self.desk_items = []

    def add_item_to_desk(self, item):
        item.in_storage = False
        self.desk_items.append(item)

    def remove_item(self, item):
        if item in self.desk_items:
            self.desk_items.remove(item)

    def get_item_at_position(self, pos):
        # 只需要检查桌面物品
        for item in reversed(self.desk_items):
            if item.contains_point(pos):
                return item
        return None

    def get_all_items(self):
        return self.desk_items

    def is_position_in_desk(self, pos):
        # 只要在屏幕右侧的大区域就算桌面
        # 稍微放宽一点判定，或者干脆只要不在传送带区域就算桌面
        x, y = pos
        return (DESK_AREA['x'] <= x <= DESK_AREA['x'] + DESK_AREA['width'] and
                DESK_AREA['y'] <= y <= DESK_AREA['y'] + DESK_AREA['height'])

    def render(self, screen):
        for item in self.desk_items:
            item.render(screen)

    # TODO (THIS PART: AI PROCESS)
    def update(self, dt):
        """物理更新 (沉重手感)"""
        # 1. 位置更新
        for item in self.desk_items:
            item.update_physics(dt)

            # 边界限制
            desk_rect = pygame.Rect(DESK_AREA['x'], DESK_AREA['y'], DESK_AREA['width'], DESK_AREA['height'])
            if not desk_rect.contains(item.get_rect()):
                if item.x < desk_rect.left:
                    item.x = desk_rect.left; item.vx = 0
                elif item.x + item.width > desk_rect.right:
                    item.x = desk_rect.right - item.width; item.vx = 0
                if item.y < desk_rect.top:
                    item.y = desk_rect.top; item.vy = 0
                elif item.y + item.height > desk_rect.bottom:
                    item.y = desk_rect.bottom - item.height; item.vy = 0
                item.set_position(item.x, item.y)

        # 2. 碰撞挤开逻辑
        push_strength = 0.3
        for i, item_a in enumerate(self.desk_items):
            for item_b in self.desk_items[i+1:]:
                if item_a.is_selected or item_b.is_selected: continue
                rect_a = item_a.get_rect().inflate(-5, -5)
                rect_b = item_b.get_rect().inflate(-5, -5)

                if rect_a.colliderect(rect_b):
                    center_a = pygame.math.Vector2(rect_a.center)
                    center_b = pygame.math.Vector2(rect_b.center)
                    diff = center_a - center_b
                    dist = diff.length()
                    if dist == 0:
                        force = pygame.math.Vector2(random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5))
                    else:
                        force = diff.normalize()

                    push_force = force * push_strength
                    item_a.vx += push_force.x; item_a.vy += push_force.y
                    item_b.vx -= push_force.x; item_b.vy -= push_force.y
                    spin = random.uniform(-0.05, 0.05)
                    item_a.va += spin; item_b.va -= spin