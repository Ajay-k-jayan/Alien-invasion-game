class GameStats:
    """track statistics for alien invasion"""

    def __init__(self, ai_game):
        """intialize statistics"""
        self.setting = ai_game.setting
        self.reset_stats()
        #start game in  an inactive state.
        self.game_active = False

        #high score should never be reset.
        self.high_score = 0

    def reset_stats(self):
        """intialize statistics that can change during the game"""
        self.ships_left = self.setting.ship_limit
        self.score = 0
        self.level = 1

