import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    #A class to represent single alien in fleet

    def __init__(self, a1_settings, screen):
        #initialize the alien and set its starting position
        super(Alien, self).__init__()
        self.screen = screen
        self.a1_settings = a1_settings

        #Load the alien image and set its rect attribute
        self.image = pygame.image.load('images\dalien.bmp')
        self.rect = self.image.get_rect()

        #start the alien near top left of screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #Store the alien position
        self.x = float(self.rect.x)

    def check_edges(self):
        #return True if alien is at edge of screen
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True   
    
    def update(self):
        #move the alien right
        self.x += (self.a1_settings.alien_speed_factor * self.a1_settings.fleet_direction)
        self.rect.x = self.x
    

    def blitme(self):
        #draw the alien at current location
        self.screen.blit(self.image, self.rect)
    


