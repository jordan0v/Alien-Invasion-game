from typing import Any
import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """Класс представляющий одного пришельца!"""

    def __init__(self, ai_game):
        """Инициализирует пришельца и задает его начальное положение."""

        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        # Загружаем изображение пришельца и получаем прямоугольник.
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()
        # Помещаем его в левый верхний угол экрана.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        # Сохранение вещественной горизонтальной позиции пришельца.
        self.x = float(self.rect.x)

    def update(self):
        """Перемещает пришельцов."""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x

    def chek_edges(self):
        """Возвращает True если пришелец находится у края экрана."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= screen_rect.left:
            return True