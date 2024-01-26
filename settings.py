class Settings():
    "Класс для хранения настроек игры!"

    def __init__(self):
        "Инициализируем настройки игры!"
        # Параметры экрана.
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        self.sheep_speed = 0.5