import pygame


class Ship():
    "Класс для управления кораблем."

    def __init__(self, ai_game):
        "Инициализация корабля и назначение его начальных координат."
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        # Загружаем изображение корабля и получаем прямоугольник.
        self.image = pygame.image.load('images/starship.bmp')
        self.rect = self.image.get_rect()
        # Каждый новый корабль появляется у нижнего края экрана.
        self.rect.midbottom = self.screen_rect.midbottom
        # Флаг перемещения корабля.
        self.moving_right = False
        self.moving_left = False
        self.x = float(self.rect.x)

    def update(self):
        "Обновляет позицию корабля с учетом флага."
        if self.moving_right:
            self.x += self.settings.sheep_speed
        if self.moving_left:
            self.x -= self.settings.sheep_speed
        self.rect.x = self.x

    def blitme(self):
        "Рисует корабль в текущей позиции"
        self.screen.blit(self.image, self.rect)