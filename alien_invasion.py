import sys
from time import sleep
import pygame
from setting import setting
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien
#from game_stats import Gamestats
class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.setting = setting()
        self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        self.setting.screen_width = self.screen.get_rect().width
        self.setting.screen_height = self.screen.get_rect().height

        pygame.display.set_caption("alien inavansion")

        #create an instance to store game statistics,
        #and create a scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        #make the play button
        self.play_button = Button(self, "play")
    def run_game(self):
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self.bullets.update()
            self._update_screen()
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
    def _check_play_button(self, mouse_pos):
        """start a new game when the players clicks play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            #reset the game settings
            self.setting.initialize_dynamic_settings()

            #reset the game statistics.
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            #get rid of any remaining aliens and bullets.
            self.aliens.empty()

            self.bullets.empty()

            #create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            #hide the mouse cursor.
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """respond to keypresses"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """respond to keypresses"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _update_bullets(self):
        """update postion of bullets and get rid of old bullets"""
        #update bullet postions
        self.bullets.update()
        # get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_collisions()

    def _check_bullet_collisions(self):
        #check for any bullets that have hit aliens.
        #if so, get rid of the bullet and the alien.
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.setting.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
            #destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.setting.increase_speed()

            #increase level.
            self.stats.level += 1
            self.sb.prep_level()


    def _fire_bullet(self):
        """create a new bullet and add it to the bullets group"""
        if len(self.bullets) < self.setting.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _create_fleet(self):
        """create the fleet of aliens"""
        #make an alien.
        #create an alien and find the number of aliens in a row
        #spacing between each alien is equal to one alien width
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_apace_x = self.setting.screen_width - (2 * alien_width)
        number_aliens_x = available_apace_x // (alien_width)

        #determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_apace_y = (self.setting.screen_height -
                             (3 * alien_height) - ship_height)
        number_rows = available_apace_y // (alien_height)

        #create the full fleet of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
         #create an alien and space it in the row.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_aliens_bottom(self):
        """check if any aliens have reached the bottom of the screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                #treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def _check_fleet_edges(self):
        """respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """drop the entire fleet and change the fleets direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.setting.fleet_drop_speed
        self.setting.fleet_direction *= -1

    def _update_aliens(self):
        """check if the fleet is at an edge
        then update the postion of all aliens in the fleet"""
        self._check_fleet_edges()
        self.aliens.update()
        #look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            print("what the fuck..... ship broken!!!")
            self._ship_hit()
        #look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()


    def _ship_hit(self):
        """respond to the being hit by an alien."""
        if self.stats.ships_left > 0:
            #decrement ships_left and update scoreboard.
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            #get rid of any remaing aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            #create a new fleet and centre the ship
            self._create_fleet()
            self.ship.center_ship()

            #pause
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _update_screen(self):
        self.screen.fill(self.setting.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        #draw the score information.
        self.sb.show_score()

        #draw the play button if thr game is inactive
        if not self.stats.game_active:
            self.play_button.dra_button()

        pygame.display.flip()
if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()