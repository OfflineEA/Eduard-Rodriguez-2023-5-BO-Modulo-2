import pygame
from pygame.sprite import Sprite
from game.components.bullet import Bullet

from game.utils.constants import SPACESHIP, SCREEN_HEIGHT, SCREEN_WIDTH

# casi Todo en pygame es un objeto
# Un personaje en mi juego es un objeto (instancia de algo)
# La nave (spaceship) es un personaje => necesito una clase


# SpaceShip es una clase derivada (hija) de Sprite

# spaceship tiene una "imagen"
class SpaceShip(Sprite):
    
    def __init__(self):
        self.image_size = (60, 90)     # Cambie el tamaño de la imagen
        self.image = pygame.transform.scale(SPACESHIP, self.image_size)
        self.image_rect = self.image.get_rect()
        # Modifico el lugar de creacion de la imagen
        self.image_rect.x = (SCREEN_WIDTH - self.image_size[0])// 2 
        self.image_rect.y = SCREEN_HEIGHT * 0.8
        self.movement = 10      # Variable para la cantidad de desplazamiento
        self.bullets = []
        self.contador = 0
        self.bullet = Bullet(self.image_rect.center)

        

    def update(self):
        self.move_controlled()

    def move_in_x (self):
        # Creamos una variable para almacenar el boton presionado
        self.keys = pygame.key.get_pressed()

        # La condicional valida cual tecla se presiona, en este caso la flecha izquierda.
        if self.keys[pygame.K_LEFT]:
            # Si se presiona, restamos a la posicion de la imagen el valor del desplazamiento
            self.image_rect.x -= self.movement
            
            # Si la posicion de la imagen es menor a 0, osea esta en el borde izquierdo
            # declaramos el valor del ancho en la posicion para cambiarlo
            if self.image_rect.x < -self.image_rect.x:
                self.image_rect.x = SCREEN_WIDTH

        # Todo lo anterior pero con la flecha derecha
        if self.keys[pygame.K_RIGHT]:
            self.image_rect.x += self.movement
            if self.image_rect.x > SCREEN_WIDTH:
                self.image_rect.x = 0

    def move_in_y (self):
    # Creamos de la misma manera para el movimiento superior e inferior
        self.keys = pygame.key.get_pressed()
        if self.keys[pygame.K_UP]:
            self.image_rect.y -= self.movement
            if self.image_rect.y < -self.image_rect.y:
                self.image_rect.y = SCREEN_HEIGHT

        if self.keys[pygame.K_DOWN]:
            self.image_rect.y += self.movement
            if self.image_rect.y > SCREEN_HEIGHT:
                self.image_rect.y = 0

    # Esta clase permite el movimiento con las flechas pero sin dejar pasar de los bordes
    def move_controlled (self):
        self.keys = pygame.key.get_pressed()
        if self.keys[pygame.K_LEFT]:
            if self.image_rect.x > 0:
                self.image_rect.x -= self.movement
                self.bullet.bullet_rect.x -= self.movement

        if self.keys[pygame.K_RIGHT]:
            if self.image_rect.x < SCREEN_WIDTH - self.image_size[0]:
                self.image_rect.x += self.movement
                self.bullet.bullet_rect.x += self.movement
        
        if self.keys[pygame.K_UP]:
            if self.image_rect.y > 0:
                self.image_rect.y -= self.movement
                self.bullet.bullet_rect.y -= self.movement
        
        if self.keys[pygame.K_DOWN]:
            if self.image_rect.y < SCREEN_HEIGHT - self.image_size[1]:
                self.image_rect.y += self.movement
                self.bullet.bullet_rect.y += self.movement



    def draw (self, screen):
        screen.blit(self.image, self.image_rect)

    def shoot (self, screen):
        self.keys_bullet = pygame.key.get_pressed()
        if self.keys_bullet[pygame.K_SPACE]:
            self.contador = 1
            
        while True:
                self.bullet.draw(screen)
                if self.contador == 1:
                    self.bullets.append(self.contador)
                    for self.items in self.bullets:
                        self.bullet.bullet_rect.y -= self.movement
                        if self.bullet.bullet_rect.y <= 0:
                            self.bullets.clear()
                            self.bullet.update()
                            self.contador = 0
                            self.bullet.bullet_rect.y = self.image_rect.y
                            break
                break

        

     
