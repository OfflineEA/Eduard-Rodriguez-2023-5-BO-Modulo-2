import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    def __init__(self, spaceship_center, bullet):
        super().__init__()
        self.bullet_size = (20, 30)
        self.bullet = pygame.transform.scale(bullet, self.bullet_size)
        self.bullet_rect = self.bullet.get_rect()
        self.movement = 10
        self.bullet_rect.center = spaceship_center

    def update(self):
        # Actualiza la posición de la bala
        self.bullet_rect.y -= self.movement
        if self.bullet_rect.y <= 0:
            self.kill()  # Elimina la bala cuando sale de la pantalla

    def draw(self, screen):
        # Dibuja la bala en la pantalla
        screen.blit(self.bullet, self.bullet_rect)