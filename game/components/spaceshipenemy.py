import pygame

from pygame.sprite import Sprite

from game.utils.constants import SPACESHIP, SCREEN_WIDTH

class SpaceShipEnemy (Sprite):
    def __init__(self, position_x, position_y):
        # self.position_x = position_x
        # self.position_y = position_y
        self.image_size_enemy = [60, 90]
        self.ship_enemy = pygame.transform.scale(SPACESHIP, self.image_size_enemy)
        self.rotated_ship_enemy = pygame.transform.rotate(self.ship_enemy, 180)
        self.image_rect_enemy = self.rotated_ship_enemy.get_rect()
        # La imagen se creara segun las siguientes coordenadas
        self.image_rect_enemy.x = position_x      # Recomendado: 520
        self.image_rect_enemy.y = position_y      # Recomendado: 110
        self.movement_enemy = 10
        self.direction_enemy = 1
    
    def update_enemy(self):
        self.move_enemy()
    
    def move_enemy(self):
        self.image_rect_enemy.x += self.movement_enemy * self.direction_enemy

        if  self.image_rect_enemy.x <= 0 or self.image_rect_enemy.x + self.image_size_enemy[0] > SCREEN_WIDTH:
            self.direction_enemy *= -1
            self.image_rect_enemy.x += self.direction_enemy
    

