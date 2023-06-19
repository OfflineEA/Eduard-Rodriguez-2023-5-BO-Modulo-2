import pygame
import random

from pygame.sprite import Sprite
from game.components.bullet import Bullet

from game.utils.constants import ENEMY_2, SCREEN_WIDTH, SCREEN_HEIGHT, BULLET_ENEMY, FONT_STYLE

class Enemy (Sprite):
    def __init__(self, position_x, position_y):
        super().__init__()
        pygame.mixer.init()
        self.image_size_enemy = (60, 90)
        self.ship_enemy = pygame.transform.scale(ENEMY_2, self.image_size_enemy)
        self.image_rect_enemy = self.ship_enemy.get_rect()
        self.image_rect_enemy.x = position_x      # Recomendado: 520
        self.image_rect_enemy.y = position_y      # Recomendado: 90
        self.movement_enemy = 15
        self.direction_enemy = 1
        self.enemy_timer = 0
        self.bullet_enemy = Bullet(self.image_rect_enemy.center, BULLET_ENEMY)
        self.hits_enemy = []
        self.counter_enemy = 0
        self.shoot_sound = pygame.mixer.Sound("Eduard-Rodriguez-2023-5-BO-Modulo-2/game/assets/Songs/Shoot_Enemy.wav")
        self.sound_damage = pygame.mixer.Sound("Eduard-Rodriguez-2023-5-BO-Modulo-2/game/assets/Songs/Received_Damage.wav")
    def update_enemy(self):
        self.move_enemy()
    
    def move_enemy(self):
        self.image_rect_enemy.x += self.movement_enemy * self.direction_enemy
        self.bullet_enemy.bullet_rect.x = self.image_rect_enemy.x + 18
        if  self.image_rect_enemy.x <= 0 or self.image_rect_enemy.x + self.image_size_enemy[0] > SCREEN_WIDTH:
            self.direction_enemy *= -1
            self.image_rect_enemy.x += self.direction_enemy
            self.bullet_enemy.bullet_rect.x = self.image_rect_enemy.x

    def draw_enemy (self, screen):
        screen.blit(self.ship_enemy, self.image_rect_enemy)
        self.status_enemy(screen)
        
    def shoot_enemy (self, screen, spaceship):
        self.current_time = pygame.time.get_ticks()
        time_between_shots = random.randrange(700, 1000, 100)
        
        if self.current_time - self.enemy_timer > time_between_shots:
            self.shoot_sound.play()
            while True:
                self.bullet_enemy.bullet_rect.y += self.movement_enemy
                self.bullet_enemy.draw(screen)
                if self.bullet_enemy.bullet_rect.colliderect(spaceship.image_rect):
                    self.shoot_sound.stop()
                    self.hit = 1
                    self.hits_enemy.append(self.hit)
                    self.hit_enemy(screen)
                    self.bullet_enemy.bullet_rect.y = self.image_rect_enemy.y + 20
                    break
                if self.bullet_enemy.bullet_rect.y >= SCREEN_HEIGHT:
                    self.shoot_sound.stop()
                    self.bullet_enemy.update()
                    self.bullet_enemy.bullet_rect.y = self.image_rect_enemy.y + 20
                    self.enemy_timer = self.current_time
                return False
    
    def hit_enemy(self, screen):
        self.sound_damage.play()
        font = pygame.font.Font(FONT_STYLE, 28)
        text = font.render(" The enemy has hit you! ", True, (255, 255, 255))
        screen.blit(text, (SCREEN_WIDTH * 0.28, SCREEN_HEIGHT * 0.40))
        pygame.display.update()
        pygame.time.delay(2000)

    def status_enemy (self, screen):
        font = pygame.font.Font(FONT_STYLE, 22)
        self.counter_enemy = len(self.hits_enemy)
        text = f" Damage received: {self.counter_enemy} "
        message = font.render(text, True, (0, 0, 0))
        message.get_rect()
        screen.blit(message, (SCREEN_WIDTH * 0.68, SCREEN_HEIGHT * 0.96))
        pygame.display.update()

    def restart_enemy (self, position_x, position_y):
        self.counter_enemy = 0
        self.hits_enemy.clear()
        self.image_rect_enemy.x = position_x      
        self.image_rect_enemy.y = position_y


