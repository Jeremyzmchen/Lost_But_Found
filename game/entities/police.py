import pygame
from game.entities.customer import Customer
from config.settings import ASSETS, WINDOW_WIDTH


class Police(Customer):
    """警察实体 - 特殊顾客，负责处理案件"""

    def __init__(self, target_slot):
        # [修改点] 移除了 'normal' 参数，以匹配 Customer 的新构造函数
        # 旧代码: super().__init__('unknown', 'normal', target_slot)
        # 新代码:
        super().__init__('unknown', target_slot)

        # 警察现在拥有和普通顾客一样的耐心值逻辑 (由 Customer 父类自动处理)

        self.wait_time = 0

        # 状态机：waiting_for_note -> waiting_for_evidence
        self.police_state = 'waiting_for_note'
        self.target_item_type = None
        self.case_id = None

        self.description = "Officer on duty.\nAny cases to report?"

        # 隐藏 "Don't Have" 按钮 (警察不能被赶走)
        self.reject_button.rect.topleft = (-1000, -1000)

    def _load_resources(self):
        try:
            path = ASSETS.get('police', 'assets/images/police.png')
            self.image = pygame.image.load(path)
            self.image = pygame.transform.scale(self.image, (375, 470))
        except:
            # 备用：画一个蓝色制服的人
            self.image = pygame.Surface((100, 100))
            self.image.fill((100, 100, 100))
            pygame.draw.circle(self.image, (20, 50, 180), (50, 50), 40)

        try:
            self.bubble_image = pygame.image.load('assets/images/icons/bubble_box.png')
        except:
            pass

    def receive_note(self, note_item):
        """接收便签，进入第二阶段"""
        self.police_state = 'waiting_for_evidence'
        self.target_item_type = note_item.sought_item_type
        self.case_id = note_item.case_id

        self.description = f"Case #{self.case_id}...\nFind the missing item."

        # 进入新阶段时重置耐心
        self.wait_time = 0

    def update(self, dt):
        super().update(dt)
        # 强制隐藏拒绝按钮
        self.reject_button.rect.topleft = (-1000, -1000)