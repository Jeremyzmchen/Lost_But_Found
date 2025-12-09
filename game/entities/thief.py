
import pygame
import random
from game.entities.customer import Customer
from config.settings import ASSETS, THIEF_WAIT_TIME, THIEF_HP, COLOR_RED


class Thief(Customer):
    """
    Special NPC thief
    - Has HP
    - unique waiting time
    """

    def __init__(self, target_x):
        # extend customer, calling init method, then rewrite it
        super().__init__('thief', target_x)

        # unique characteristics
        self.max_wait_time = THIEF_WAIT_TIME
        self.patience = 1.0

        # Init HP
        self.hp = THIEF_HP
        self.is_leaving = False

        # Init img
        self._load_thief_image()

        # Remove reject button
        if self.reject_button:
            self.reject_button.rect.topleft = (-9999, -9999)

    def update(self, dt):
        """
        rewrite method
        """
        # extend update
        super().update(dt)

        # remove reject button
        if self.reject_button:
            self.reject_button.rect.topleft = (-9999, -9999)

    def _load_thief_image(self):
        """Load img"""
        try:
            path = ASSETS.get('thief', 'assets/images/thief.png')
            img = pygame.image.load(path)
            self.image = pygame.transform.scale(img, (375, 470))
        except Exception as e:
            print(f"Failed to load the conveyor belt image: {e}")

    def _generate_description(self):
        """description"""
        return "Bro, give me money!!!"

    def take_damage(self):
        """count hp"""
        self.hp -= 1

        # when hit, change description
        self.description = f"Ouch! ({self.hp} left)"

        if self.hp <= 0:
            return True
        return False

    def check_item_match(self, item):
        """thief can match anything"""
        return True