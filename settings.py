class Settings():
    """Класс для хранения настроек игры!"""

    def __init__(self):
        """Инициализируем настройки игры!"""
        # Параметры экрана.
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        self.sheep_speed = 1.5

        # Параметры снаряда.
        self.bullet_speed = 1.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullet_allowed = 3

        # Параметры пришельцов
        self.alien_speed = 1
        self.fleet_drop_speed = 20
        # fleet_direction = 1 обозначает движение вправо, а -1 влево.
        self.fleet_direction = 1

        # Настройки корабля
        self.ship_limit = 3
