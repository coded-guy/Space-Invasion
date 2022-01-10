import pygame
from pygame.sprite import Sprite

class Ship(Sprite):

    def __init__(self, a1_settings, screen):
        super(Ship, self).__init__() 

        self.screen = screen
        self.a1_settings = a1_settings

        #Load ship and get its rect
        self.image = pygame.image.load('images\ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        #Start each new ship at the bottom center of screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        #store a decimal value for ship's center
        self.center = float(self.rect.centerx)

        #Movement flags
        self.moving_right = False
        self.moving_left = False

    def update(self):
        #update ships position based on movement flags

        #update ships center value, not the rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.a1_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0 :
            self.center -= self.a1_settings.ship_speed_factor
        
        #update rect object from self.center
        self.rect.centerx = self.center

    def blitme(self):
        #draw the ship at its current position
        self.screen.blit(self.image, self.rect)
    
    def center_ship(self):
        #center ship on screen
        self.center = self.screen_rect.centerx