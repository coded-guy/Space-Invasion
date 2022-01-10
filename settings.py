class Settings():

    def __init__(self):
        #screen settings - static
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        #ship Settings
        self.ship_limit = 3

        #bullet Settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3

        #Alien settings
        self.fleet_drop_speed = 10
        
        #game speed by level up
        self.speedup_scale = 1.1

        #double the score
        self.score_scale = 2.0

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 2
        self.alien_speed_factor = 1
        #fleet direction of 1 represents right while -1 represents left
        self.fleet_direction = 1
        self.alien_points = 50
    
    def increase_speed(self):
        #increase speed Settings
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)
