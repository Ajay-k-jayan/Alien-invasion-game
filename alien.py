import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """a class to represent a single alien in the fleet"""

    def __init__(self, ai_game):
        """intialize the alien and set its starting postion"""
        super().__init__()
        self.screen = ai_game.screen
        self.setting = ai_game.setting

        #load the alien image and sets its rect attribute.
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        #start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #store the alieans exact horizontal position.
        self.x = float(self.rect.x)
    def check_edges(self):
        """return true if alien is at edge of screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """move the alien to the right or left"""
        self.x += (self.setting.alien_speed *
                   self.setting.fleet_direction)
        self.rect.x = self.x