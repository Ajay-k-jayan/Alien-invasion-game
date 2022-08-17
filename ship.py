import pygame
from pygame.sprite import Sprite
class Ship(Sprite):
    def __init__(self,ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.setting = ai_game.setting
        self.screen_rect = ai_game.screen.get_rect()
        #load ship image
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        #start ship at the bottom centre
        self.rect.midbottom = self.screen_rect.midbottom

        #store a decimal value for the ships horizontal position
        self.x = float(self.rect.x)

        #movement flag
        self.moving_right = False
        self.moving_left = False

    def center_ship(self):
        """center the ship on the screen"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)


    def update(self):
        """update the ships postion based on the movement flag"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.setting.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.setting.ship_speed

        #update rect object  from self.x
        self.rect.x = self.x




    def blitme(self):
        self.screen.blit(self.image, self.rect)
