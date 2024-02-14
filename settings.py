class Settings():
    """Класс для хранения настроек игры!"""

    def __init__(self):
        """Инициализируем статические настройки игры!"""
        # Параметры экрана.
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        # Параметры снаряда.
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullet_allowed = 3
        # Параметры пришельцов.
        self.fleet_drop_speed = 8
        # Настройки корабля.
        self.ship_limit = 3
        # Темп ускорения игры.
        self.speedup_scale = 1.5
        # Темп ускрорения набора очков.
        self.score_scale = 1.5
        self.initialize_dynamic_settings()
        # Флаг для паузы.
        self.on_pause = False

    def initialize_dynamic_settings(self):
        """Инициализирует настройки которые меняются по ходу игры!"""
        self.ship_speed = 1.5
        self.bullet_speed = 1.5
        self.alien_speed = 0.8
        # Подосчет очков.
        self.alien_points = 50
        # fleet_direction = 1 обозначает движение вправо, а -1 влево.
        self.fleet_direction = 1

    def increase_speed(self):
        """Увеличивает настройки скорости и стоимость пришельцев."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)