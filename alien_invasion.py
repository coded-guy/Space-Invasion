import sys
import pygame
from pygame.display import set_caption
from settings import Settings
from game_stats import Gamestats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from alien import Alien
import game_functions as gf
from pygame.sprite import Group


def run_game():
    #Initialize game and create a screen object
    pygame.init()
    a1_settings = Settings()
    screen = pygame.display.set_mode((a1_settings.screen_width, a1_settings.screen_height))
    pygame.display.set_caption("ALIEN INVASION")

    #Make the play button 
    play_button = Button(a1_settings, screen, "Play")

    #create an instance to store game statistics
    stats = Gamestats(a1_settings)
    sb = Scoreboard(a1_settings, screen, stats)

    #Make a ship 
    ship = Ship(a1_settings, screen)
    
    #Make a group to store bullets in
    bullets = Group()

    #Make group of aliens
    aliens = Group()

    #Create the group of aliens
    gf.create_fleet(a1_settings, screen, ship, aliens)

    #Start the main loop for the game
    while True:
        gf.check_events(a1_settings, screen, stats, sb, play_button, ship, aliens, bullets)

        if stats.game_active:
            ship.update()
            gf.update_bullets(a1_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(a1_settings,stats, screen, sb, ship, aliens, bullets)
            gf.update_screen(a1_settings, screen, stats, sb, ship, aliens, bullets, play_button)
       
run_game()