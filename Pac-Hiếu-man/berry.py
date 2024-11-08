# berry.py
import pygame
from settings import CHAR_SIZE, PLAYER_SPEED

class Berry(pygame.sprite.Sprite):
    def __init__(self, row, col, size, is_power_up=False):
        super().__init__()
        self.power_up = is_power_up
        self.size = size
        self.color = pygame.Color("violetred")
        self.thickness = size
        self.abs_x = (row * CHAR_SIZE) + (CHAR_SIZE // 2)
        self.abs_y = (col * CHAR_SIZE) + (CHAR_SIZE // 2)
        # temporary rect for colliderect-checking
        self.rect = pygame.Rect(self.abs_x - self.size, self.abs_y - self.size, self.size * 2, self.size * 2)

    def update(self, screen):
        # Draw the circle and update the rect for collision detection
        pygame.draw.circle(screen, self.color, (self.abs_x, self.abs_y), self.size, self.thickness)
        self.rect.topleft = (self.abs_x - self.size, self.abs_y - self.size)  # Update rect position

