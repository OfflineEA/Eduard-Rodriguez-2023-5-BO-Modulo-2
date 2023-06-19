import pygame
from pygame.sprite import Sprite
from game.components.bullet import Bullet
from game.components.enemy import Enemy

from game.utils.constants import SPACESHIP, SCREEN_HEIGHT, SCREEN_WIDTH, BULLET, FONT_STYLE

class SpaceShip(Sprite):
    
    def __init__(self):
        super().__init__()
        self.image_size = (60, 90)
        self.image = pygame.transform.scale(SPACESHIP, self.image_size)
        self.image_rect = self.image.get_rect()
        self.image_rect.x = (SCREEN_WIDTH - self.image_size[0])// 2 
        self.image_rect.y = SCREEN_HEIGHT * 0.8
        self.movement = 15 
        self.bullets = []
        self.hits = []
        self.bullet = Bullet(self.image_rect.center, BULLET)
        self.enemy = Enemy(520, 90)
        self.bullet_counter = 0

    def update(self):
        self.move_controlled()
        self.enemy.update_enemy()

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
            if self.image_rect.y > 300:
                self.image_rect.y -= self.movement
                self.bullet.bullet_rect.y -= self.movement
        
        if self.keys[pygame.K_DOWN]:
            if self.image_rect.y < SCREEN_HEIGHT - 130:
                self.image_rect.y += self.movement
                self.bullet.bullet_rect.y += self.movement

    def draw (self, screen):
        screen.blit(self.image, self.image_rect)
        self.status(screen)

    def shoot (self, screen):
        self.keys_bullet = pygame.key.get_pressed()
        if self.keys_bullet[pygame.K_SPACE]:
            self.bullet_counter = 1
            
        while True:
            self.bullet.draw(screen)
            if self.bullet_counter == 1:
                self.bullets.append(self.bullet_counter)
                for self.items in self.bullets:
                    self.bullet.bullet_rect.y -= self.movement
                    if self.bullet.bullet_rect.colliderect(self.enemy.image_rect_enemy):
                        self.bullets.clear()
                        self.bullet.update()
                        self.bullet_counter = 0
                        self.hits.append(self.bullet_counter)
                        self.hits_spaceship(screen)
                        self.bullet.bullet_rect.y = self.image_rect.y
                        break
                    if self.bullet.bullet_rect.y <= 0:
                        self.bullets.clear()
                        self.bullet.update()
                        self.bullet_counter = 0
                        self.bullet.bullet_rect.y = self.image_rect.y
                        break
            break

    def hits_spaceship(self, screen):
        font = pygame.font.Font(FONT_STYLE, 28)
        text = font.render("Haz golpeado al enemigo!", True, (255, 255, 255))
        screen.blit(text, (SCREEN_WIDTH * 0.35, SCREEN_HEIGHT * 0.40))
        pygame.display.update()
        pygame.time.delay(2000)      

    def status (self, screen):
        font = pygame.font.Font(FONT_STYLE, 22)
        self.counter = len(self.hits)
        text = f" Times you hit the enemy: {self.counter} "
        message = font.render(text, True, (0, 0, 0))
        message.get_rect()
        screen.blit(message, (0, SCREEN_HEIGHT * 0.96))
        pygame.display.update()
    
    def restart (self):
        self.hits.clear()
        self.counter = 0
        pygame.display.update()
        



        


        

     
