class GameStats():
    """Отслеживание статистики для игры GameInvasion."""

    def __init__(self, ai_game):
        """Инициализирует статистику."""
        self.settings = ai_game.settings
        self.reset_stats()
        # Игра запускается в неактивном состоянии.
        self.game_active = False
        # Инициализируем рекордный счет.
        self.high_score = 0

    def reset_stats(self):
        """Инициализирует статистику, изменяющуюся по ходу игры!"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1