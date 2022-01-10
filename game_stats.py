class Gamestats():
    #track stats for alien invasion

    def __init__(self, a1_settings):
        #initialize stats 
        self.a1_settings = a1_settings
        self.reset_stats()
        self.game_active = True
        self.high_score = 0

    def reset_stats(self):
        #initialize stats that can change during the game
        self.ships_left = self.a1_settings.ship_limit 
        self.score = 0
        self.level = 1
