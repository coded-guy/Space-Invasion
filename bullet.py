import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    #class to manage bullets fired from the ship

    def __init__(self, a1_settings, screen, ship):
        #create a bullet object at ships current position
        super(Bullet, self).__init__()
        self.screen = screen

        #create a bullet rect at (0, 0) and then set correct position
        self.rect = pygame.Rect(0, 0, a1_settings.bullet_width, a1_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        #Store the bullet's position as a decimal value
        self.y = float(self.rect.y)

        self.color = a1_settings.bullet_color
        self.speed_factor = a1_settings.bullet_speed_factor
    
    def update(self):
        #update the bullet position
        self.y -= self.speed_factor
        #update the rect position
        self.rect.y = self.y

    def draw_bullet(self):
        #draw the bullet to the screen
        pygame.draw.rect(self.screen, self.color, self.rect)