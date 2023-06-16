import pygame

from pygame.sprite import Sprite

from game.utils.constants import ENEMY_2, SCREEN_WIDTH

class Enemy (Sprite):
    def __init__(self, position_x, position_y):
        self.image_size_enemy = (60, 90)
        self.ship_enemy = pygame.transform.scale(ENEMY_2, self.image_size_enemy)
        self.image_rect_enemy = self.ship_enemy.get_rect()
        # La imagen se creara segun las coordenadas digitadas
        self.image_rect_enemy.x = position_x      # Recomendado: 520
        self.image_rect_enemy.y = position_y      # Recomendado: 110
        self.movement_enemy = 10
        self.direction_enemy = 1    # Variable que permite cambiar la direccion
        # self.hitbox_enemy = pygame.Rect(self.image_rect_enemy.x, self.image_rect_enemy.y, self.image_size_enemy[0], self.image_size_enemy[1])
    
    def update_enemy(self):
        self.move_enemy()
    
    # Creamos un metodo para mover los enemigos
    def move_enemy(self):
        # Actualizamos el valor en el eje x
        self.image_rect_enemy.x += self.movement_enemy * self.direction_enemy
        # La condicional valida si la imagen esta en algun borde
        if  self.image_rect_enemy.x <= 0 or self.image_rect_enemy.x + self.image_size_enemy[0] > SCREEN_WIDTH:
            # Al cumplirse la condicion el enemigo cambia de direccion
            self.direction_enemy *= -1
            self.image_rect_enemy.x += self.direction_enemy

    

