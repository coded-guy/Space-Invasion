import sys
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien



def check_keydown_events(event, a1_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(a1_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def fire_bullet(a1_settings, screen, ship, bullets):
    #create new bullet and add it to the bullets group
    if len(bullets) < a1_settings.bullets_allowed:
        new_bullet = Bullet(a1_settings, screen, ship)
        bullets.add(new_bullet)


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(a1_settings, screen, stats, sb, play_button, ship, aliens, bullets): 
    #responds to keypress and mouse events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, a1_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(a1_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)
        
def check_play_button(a1_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    #start game when player clicks play button
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        a1_settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True

        #reset the score board images
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        #empty list of aliens and bullets_allowed
        aliens.empty()
        bullets.empty()

        #create a new fleet and center ship
        create_fleet(a1_settings, screen, ship, aliens)
        ship.center_ship()

def update_bullets(a1_settings, screen, stats, sb, ship, aliens, bullets):
    #update bullet positions
    bullets.update()

    #Get rid of bullets that have crossed the top of screen
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
        
    check_bullet_alien_collisions(a1_settings, screen, stats, sb, ship, aliens, bullets)

def check_bullet_alien_collisions(a1_settings, screen, stats, sb, ship, aliens, bullets):
    #remove  any bullets and aliens that have collided
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += a1_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
    
    if len(aliens) == 0:
        #destroy existing bullets and create new fleet
        bullets.empty()
        a1_settings.increase_speed()
        stats.level += 1
        sb.prep_level()

        create_fleet(a1_settings, screen, ship, aliens)

def update_screen(a1_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    #Redraw the screen during each pass thru the loop
    screen.fill(a1_settings.bg_color)
    ship.blitme()

    #Redraw all bullets behind ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    #draw the score information
    sb.show_score()

    #draw the play button if game is inactive
    if not stats.game_active:
        play_button.draw_button()
 
    #Make the most recently drawn screen visible
    pygame.display.flip()

def get_number_aliens_x(a1_settings, alien_width):
    #determine number of aliens that fit row
    available_space_x = a1_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(a1_settings, ship_height, alien_height):
    #Determine the number of rows of aliens that fit on the screen
    available_space_y = (a1_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(a1_settings, screen, aliens, alien_number, row_number):
    #create an alien then place in row
    alien = Alien(a1_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(a1_settings, screen, ship, aliens):
    #create fleet of aliens and find no. of aliens in a row. spacing btwn each alien is == one alien width
    alien = Alien(a1_settings, screen)
    number_aliens_x = get_number_aliens_x(a1_settings, alien.rect.width)
    number_rows = get_number_rows(a1_settings, ship.rect.height, alien.rect.height)
    

    #create the first row of aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(a1_settings, screen, aliens, alien_number, row_number)

def check_fleet_edges(a1_settings, aliens):
    #resspond appropriately if any aliens have reached an edge
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(a1_settings, aliens)
            break

def change_fleet_direction(a1_settings, aliens):
    #drop the entire fleet and change fleet direction
    for alien in aliens.sprites():
        alien.rect.y += a1_settings.fleet_drop_speed
    a1_settings.fleet_direction *= -1

def ship_hit(a1_settings, stats, screen, sb, ship, aliens, bullets):
    #respond to ship being hit by aliens
    if stats.ships_left > 0:
        stats.ships_left -= 1

        sb.prep_ships()

        #empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        #create a new fleet and center the ships
        create_fleet(a1_settings, screen, ship, aliens)
        ship.center_ship()

        #pause
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(a1_settings, stats, screen, sb, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(a1_settings, stats, screen, sb, ship, aliens, bullets)
            break

def update_aliens(a1_settings, stats, screen, sb, ship, aliens, bullets):
    #update the positions of all aliens in the fleet
    check_fleet_edges(a1_settings, aliens)
    aliens.update()

    #look for alien-ship collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(a1_settings, stats, screen, sb, ship, aliens, bullets)

    check_aliens_bottom(a1_settings, stats, screen, sb, ship, aliens, bullets)

def check_high_score(stats, sb):
    #check to see if theres a new high score
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()