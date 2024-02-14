import sys
import pygame
from time import sleep

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

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
        # Создание экземпляра для хранения игровой статистики.
        self.stats = GameStats(self)
        # Создание панели для отображения статистики.
        self.sb = Scoreboard(self)
        # Инициализация объекта космического корабля.
        self.ship = Ship(self)
        # Инициализация группы снарядов для их управления.
        self.bullets = pygame.sprite.Group()
        # Инициализация группы пришельцов для их управления.
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        # Создание кнопки Play.
        self.play_button = Button(self, "Play")


    def run_game(self):
        """Запуск основного цикла игры!"""
        while True:
            self._chek_events()
            if self.stats.game_active and not self.settings.on_pause:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Запускает новую игру при нажатии на кнопку Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Сброс игровых настроек.
            self.settings.initialize_dynamic_settings()
            # Запускает игру заново.
            self.start_game()

    def start_game(self):
        # Сброс игровой статистики.
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ship()
            self.settings.initialize_dynamic_settings()
            # Очистка списков пришельцов и снарядов.
            self.aliens.empty()
            self.bullets.empty()
            # Создание нового флота и размещения корабля в центре.
            self._create_fleet()
            self.ship.center_ship()
            # Скрытие указателя мыши во время игры.
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        # Реагирует на нажатие клавиши.
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_p:
            self.start_game()
        elif event.key == pygame.K_s or event.key == pygame.K_ESCAPE:
            if self.settings.on_pause == False:
                self.settings.on_pause = True
            elif self.settings.on_pause == True:
                self.settings.on_pause = False
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

    def _create_fleet(self):
        """Создание флота пришельцов."""
        # Создание пришельца.
        # Интервал между пришельцами равен ширине пришельца.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        # Определяет количество пришельцов в ряду.
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        # Определяет количество рядов пришельцов.
        ship_height = self.ship.rect.height
        available_space_y = self.settings.screen_height - \
            (3 * alien_height) - ship_height
        number_rows = available_space_y // (2 * alien_height)
        # Создание рядов пришельцов.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Создание пришельца и размещение его в ряду."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 2 * alien_height * row_number
        self.aliens.add(alien)

    def _chek_fleet_edges(self):
        """Реагирует на достижение пришельцом края экрана."""
        for alien in self.aliens.sprites():
            if alien.chek_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Опускает весь флот и меняет направление флота."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """Обновляет изображения на экране и отображает новый экран."""
        # При каждом проходе цикла перерисовывается экран.
        self.screen.fill(self.settings.bg_color)
        # Отрисовываем корабль на экран.
        self.ship.blitme()
        # Выводим пули на экран.
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        # Отрисовываем корабли пришельцов.
        self.aliens.draw(self.screen)
        # Выводит информацию о счете.
        self.sb.show_score()
        # Кнопка Play отображается если игра неактивна.
        if not self.stats.game_active:
            self.play_button.draw_button()
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
        # Проверка попаданий в пришельцев.
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Обработка коллизий снарядов с пришельцами."""
        # Удаление снарядов и пришельцев, учавствующих в коллизиях.
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
            # Уничтожение существующих снарядов, повышение скорости и создание нового флота.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            # Увеличение уровня.
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        """Проверяет достиг ли флот края экрана и затем
        обновляет позицию каждого пришельца."""
        self._chek_fleet_edges()
        self.aliens.update()
        # Проверка коллизий "пришелец - корабль"
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        # Проверяет добрались ли пришельцы до нижнего края.
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """Проверяет добрались ли пришельцы до края экрана."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _ship_hit(self):
        """Обрабатывает столкновения корабля с пришельцами."""
        if self.stats.ships_left > 0:
            # Уменьшаем количество оставшихся кораблей и обновляет панель счета.
            self.stats.ships_left -= 1
            self.sb.prep_ship()
            # Очистка списков пришельцев и снарядов.
            self.aliens.empty()
            self.bullets.empty()
            # Создание нового флота и размещение корабля в центре.
            self._create_fleet()
            self.ship.center_ship()
            # Пауза
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
