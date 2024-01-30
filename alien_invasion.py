import sys
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet


class AlienInvasion:
    """Класс для управления ресурсами и поведением игры!!!"""

    def __init__(self):
        """Инициальзируем игру и создаем игровые ресурсы!"""
        pygame.init()

        self.settings = Settings()
        """Режим в окне --->"""
        # self.screen = pygame.display.set_mode(
        #     (self.settings.screen_width, self.settings.screen_height))
        """Полноэкранный режим --->"""
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        pygame.display.set_caption("Alien Invasion")
        # Инициализация объекта космического корабля.
        self.ship = Ship(self)
        # Инициализация группы снарядов для их управления.
        self.bullets = pygame.sprite.Group()

    def run_game(self):
        """Запуск основного цикла игры!"""
        while True:
            self._chek_events()
            self.ship.update()
            self._update_bullets()
            self._update_screen()

    def _chek_events(self):
        # Обрабатывает нажатия клавиш и события мыши.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        # Реагирует на нажатие клавиши.
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        # Реагирует на отпускание клавиши.
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Создание нового снаряда и включение его в группу снарядов."""
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_screen(self):
        """Обновляет изображения на экране и отображает новый экран"""
        # При каждом проходе цикла перерисовывается экран.
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        # Отображение последнего прорисованного экрана
        pygame.display.flip()

    def _update_bullets(self):
        """Обновляет позиции снарядов и удаляет старые."""
        # Обновление позиции снарядов.
        self.bullets.update()
        # Удаление снарядов вышедших за край экрана.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
