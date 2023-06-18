import pygame
import random

from pygame.sprite import Sprite
from game.components.bullet import Bullet


from game.utils.constants import ENEMY_2, SCREEN_WIDTH, SCREEN_HEIGHT

class Enemy (Sprite):
    def __init__(self):
        super().__init__()
        self.image_size_enemy = (60, 90)
        self.ship_enemy = pygame.transform.scale(ENEMY_2, self.image_size_enemy)
        self.image_rect_enemy = self.ship_enemy.get_rect()
        # La imagen se creara segun las coordenadas digitadas
        self.image_rect_enemy.x = 520      # Recomendado: 520
        self.image_rect_enemy.y = 90      # Recomendado: 110
        self.movement_enemy = 15
        self.direction_enemy = 1
        self.enemy_timer = 0
        self.bullet_enemy = Bullet(self.image_rect_enemy.center)
        #self.bullets = pygame.sprite.Group()
        self.hits_enemy = []


    def update_enemy(self):
        self.move_enemy()
        # self.colision()
        #self.shoot_enemy()
    
    # Creamos un metodo para mover los enemigos
    def move_enemy(self):
        # Actualizamos el valor en el eje x
        self.image_rect_enemy.x += self.movement_enemy * self.direction_enemy
        self.bullet_enemy.bullet_rect.x = self.image_rect_enemy.x + 18
        # La condicional valida si la imagen esta en algun borde
        if  self.image_rect_enemy.x <= 0 or self.image_rect_enemy.x + self.image_size_enemy[0] > SCREEN_WIDTH:
            # Al cumplirse la condicion el enemigo cambia de direccion
            self.direction_enemy *= -1
            self.image_rect_enemy.x += self.direction_enemy
            self.bullet_enemy.bullet_rect.x = self.image_rect_enemy.x

    def draw_enemy (self, screen):
        screen.blit(self.ship_enemy, self.image_rect_enemy)
        

    def shoot_enemy (self, screen):
        # from game.components.spaceship import SpaceShip
        # self.spaceship = SpaceShip()

        self.current_time = pygame.time.get_ticks()
        time_between_shots = random.randrange(500, 1000, 100)
        if self.current_time - self.enemy_timer > time_between_shots:
            while True:
                self.bullet_enemy.draw(screen)
                #self.spaceship.update()
                self.bullet_enemy.bullet_rect.y += self.movement_enemy
                # if self.bullet_enemy.bullet_rect.colliderect(self.spaceship.image_rect):
                #     self.contador = 1
                #     self.hits_enemy.append(self.contador)
                #     print(self.hits_enemy)
                #     self.hit_enemy(screen)
                #     self.bullet_enemy.bullet_rect.y = self.image_rect_enemy.y + 20
                #     break
                if self.bullet_enemy.bullet_rect.y >= SCREEN_HEIGHT:
                    self.bullet_enemy.update()
                    self.bullet_enemy.bullet_rect.y = self.image_rect_enemy.y + 20
                    self.enemy_timer = self.current_time
                return False
    
    def hit_enemy(self, screen):
        font = pygame.font.Font(None, 36)
        text = font.render("El enemigo te ha golpeado!...", True, (255, 255, 255))
        screen.blit(text, (SCREEN_WIDTH * 0.35, SCREEN_HEIGHT * 0.40))
        pygame.display.flip()
        pygame.time.delay(2000)