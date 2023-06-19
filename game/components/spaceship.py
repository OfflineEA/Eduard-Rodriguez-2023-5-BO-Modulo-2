import pygame
import random
from pygame.sprite import Sprite
from game.components.bullet import Bullet
from game.components.enemy import Enemy

from game.utils.constants import SPACESHIP, SCREEN_HEIGHT, SCREEN_WIDTH, BULLET, SPACESHIP_DAMAGE, BULLET_DOUBLE, FONT_STYLE

class SpaceShip(Sprite):
    
    def __init__(self):
        super().__init__()
        pygame.mixer.init()
        self.image_size = (60, 90)
        self.image = pygame.transform.scale(SPACESHIP, self.image_size)
        self.image_weapon = pygame.transform.scale(SPACESHIP_DAMAGE, self.image_size)
        self.image_rect = self.image.get_rect()
        self.image_rect.x = (SCREEN_WIDTH - self.image_size[0])// 2 
        self.image_rect.y = SCREEN_HEIGHT * 0.8
        self.movement = 15 
        self.bullets = []
        self.hits = []
        self.bullet = Bullet(self.image_rect.center, BULLET)
        self.enemy = Enemy(520, 90)
        self.counter = 0
        self.bullet_counter = 0
        self.random_counter = random.randrange(3, 5)
        self.current_spaceship = 0
        self.weapon_duration = 1  # Duración del escudo
        self.weapon_counter = 0
        self.failed_attack = False

        self.shoot_sound = pygame.mixer.Sound("Eduard-Rodriguez-2023-5-BO-Modulo-2/game/assets/Songs/Shoot.wav")
        self.power_shoot_sound = pygame.mixer.Sound("Eduard-Rodriguez-2023-5-BO-Modulo-2/game/assets/Songs/Shoot_Double.wav")

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
        self.status(screen)
        if self.current_spaceship == 0:
            screen.blit(self.image, self.image_rect)
        elif self.current_spaceship == 1:
            screen.blit(self.image_weapon, self.image_rect)
            if self.weapon_counter > self.weapon_duration:
                self.hits.append(self.current_spaceship)
                self.broken_weapon(screen)
                self.current_spaceship = 0
                self.failed_attack = False
            elif self.failed_attack:
                self.broken_weapon(screen)
                self.current_spaceship = 0

    def shoot (self, screen):
        self.keys_bullet = pygame.key.get_pressed()
            
        if self.keys_bullet[pygame.K_SPACE]:
            self.sound_shoot()
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
                        self.counter = self.counter + 1
                        self.bullet_counter = 0
                        self.hits.append(self.bullet_counter)
                        self.hits_spaceship(screen)
                        self.weapon_counter += 1
                        self.bullet.bullet_rect.y = self.image_rect.y + 5
                        break
                    if self.bullet.bullet_rect.y <= 0:
                        self.bullets.clear()
                        self.bullet.update()
                        self.bullet_counter = 0
                        self.bullet.bullet_rect.y = self.image_rect.y + 5
                        if self.current_spaceship == 1:
                            self.failed_attack = True
                        break
            break

    def hits_spaceship(self, screen):
        if self.current_spaceship == 0:
            font = pygame.font.Font(FONT_STYLE, 28)
            text = font.render("You have hit the enemy!", True, (255, 255, 255))
            screen.blit(text, (SCREEN_WIDTH * 0.35, SCREEN_HEIGHT * 0.40))
            pygame.display.update()
            pygame.time.delay(2000)
        elif self.current_spaceship == 1:
            font = pygame.font.Font(FONT_STYLE, 28)
            text = font.render("You dealt an attack with double damage!", True, (255, 255, 255))
            screen.blit(text, (SCREEN_WIDTH * 0.25, SCREEN_HEIGHT * 0.45))
            pygame.display.update()
            pygame.time.delay(2000)
            self.weapon_counter += 1

    def status (self, screen):
        font = pygame.font.Font(FONT_STYLE, 22)
        text = f" Times you hit the enemy: {len(self.hits)} "
        message = font.render(text, True, (0, 0, 0))
        message.get_rect()
        screen.blit(message, (0, SCREEN_HEIGHT * 0.96))
        pygame.display.update()
        if self.counter == self.random_counter:
            self.current_spaceship = 1
            self.weapon_power(screen)
            self.random_counter -= 1


    def weapon_power (self, screen):
        self.weapon_counter = 0
        font = pygame.font.Font(FONT_STYLE, 28)
        text = f" You take DOUBLE DAMAGE for one hit! "
        message_weapon = font.render(text, True, (255, 255, 255))
        message_weapon.get_rect()
        icon = pygame.transform.scale(BULLET_DOUBLE, (50, 80))
        screen.blit(icon, (525, SCREEN_HEIGHT * 0.25))
        screen.blit(message_weapon, (SCREEN_WIDTH * 0.25, SCREEN_HEIGHT * 0.45))
        pygame.display.update()
        pygame.time.delay(1500)
    
    def broken_weapon(self, screen):
        font = pygame.font.Font(FONT_STYLE, 28)
        text = f" You've used your power-up! "
        message_weapon = font.render(text, True, (255, 255, 255))
        message_weapon.get_rect()
        screen.blit(message_weapon, (SCREEN_WIDTH * 0.35, SCREEN_HEIGHT * 0.30))
        pygame.display.update()
        pygame.time.delay(1000)
        self.counter = 0

    def sound_shoot(self):
        if self.current_spaceship == 0:
            self.shoot_sound.play()
        elif self.current_spaceship == 1:
            self.power_shoot_sound.play()

    def restart (self):
        self.hits.clear()
        self.counter = 0
        



        


        

     
