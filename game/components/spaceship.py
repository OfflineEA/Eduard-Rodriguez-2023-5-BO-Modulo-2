import pygame
import random
from pygame.sprite import Sprite
from game.components.bullet import Bullet

from game.utils.constants import SPACESHIP, SCREEN_HEIGHT, SCREEN_WIDTH, BULLET, SPACESHIP_DAMAGE, BULLET_DOUBLE, FONT_STYLE

class SpaceShip(Sprite):
    
    def __init__(self):
        super().__init__()
        pygame.mixer.init()
        self.image_size = (60, 90)
        self.image = pygame.transform.scale(SPACESHIP, self.image_size)
        self.image_weapon = pygame.transform.scale(SPACESHIP_DAMAGE, self.image_size)
        self.image_rect = self.image.get_rect()
        self.image_rect.x = (SCREEN_WIDTH - self.image_size[0]) // 2 
        self.image_rect.y = SCREEN_HEIGHT * 0.8
        self.movement = 10 
        self.bullets = []
        self.hits = []
        self.bullet = Bullet(self.image_rect.center, BULLET)
        self.counter = 0
        self.bullet_counter = 0
        self.random_counter = random.randrange(3, 5)
        self.current_spaceship = 0
        self.weapon_duration = 1  
        self.weapon_counter = 0
        self.failed_attack = False
        self.shoot_sound = pygame.mixer.Sound("Eduard-Rodriguez-2023-5-BO-Modulo-2/game/assets/Songs/Shoot.wav")
        self.power_shoot_sound = pygame.mixer.Sound("Eduard-Rodriguez-2023-5-BO-Modulo-2/game/assets/Songs/Shoot_Double.wav")
        self.shoot_sound.set_volume(0.2)
        self.power_shoot_sound.set_volume(0.2)

    def update(self):
        self.move_controlled()

    def move_controlled(self):
        # Movimiento controlado por las teclas
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

    def draw(self, screen):
        # Dibujar la nave espacial y mostrar mensajes de poder
        self.draw_status(screen)
        if self.current_spaceship == 0:
            screen.blit(self.image, self.image_rect)
        elif self.current_spaceship == 1:
            screen.blit(self.image_weapon, self.image_rect)
            if self.weapon_counter > self.weapon_duration:
                self.hits.append(self.current_spaceship)
                self.draw_finish_power(screen)
                self.current_spaceship = 0
                self.failed_attack = False
            elif self.failed_attack:
                self.draw_finish_power(screen)
                self.current_spaceship = 0

    def shoot(self, screen, enemy):
        # Disparar y manejar colisiones de balas
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
                    if self.bullet.bullet_rect.colliderect(enemy.image_rect_enemy):
                        self.bullets.clear()
                        self.bullet.update()
                        self.counter = self.counter + 1
                        self.bullet_counter = 0
                        self.hits.append(self.bullet_counter)
                        self.draw_hits_spaceship(screen)
                        self.weapon_counter += 1
                        self.bullet.bullet_rect.y = self.image_rect.y + 5
                        break
                    if self.bullet.bullet_rect.y <= 0:
                        if self.current_spaceship == 1:
                            self.failed_attack = True
                        self.bullets.clear()
                        self.bullet.update()
                        self.bullet_counter = 0
                        self.bullet.bullet_rect.y = self.image_rect.y + 5
                        break
            break

    def draw_hits_spaceship(self, screen):
        # Dibujar mensajes de golpe a la nave espacial
        messages = [
            "You have hit the enemy!",
            "You dealt an attack with double damage!"
        ]
        positions = [
            (SCREEN_WIDTH * 0.28, SCREEN_HEIGHT * 0.40),
            (SCREEN_WIDTH * 0.10, SCREEN_HEIGHT * 0.45)
        ]
        self.weapon_counter += self.current_spaceship == 1
        font = pygame.font.Font(FONT_STYLE, 28)
        text = font.render(messages[self.current_spaceship], True, (255, 255, 255))
        screen.blit(text, positions[self.current_spaceship])
        pygame.display.update()
        pygame.time.delay(2000)

    def draw_status(self, screen):
        # Dibujar la puntuación y mensajes de poder
        font = pygame.font.Font(FONT_STYLE, 22)
        text = f" New high score: {len(self.hits)} "
        message = font.render(text, True, (0, 0, 0))
        message.get_rect()
        screen.blit(message, (0, SCREEN_HEIGHT * 0.96))
        if self.counter == self.random_counter:
            self.current_spaceship = 1
            self.draw_message_power(screen)
            self.random_counter -= 1

    def draw_message_power(self, screen):
        # Mostrar mensaje de poder
        self.weapon_counter = 0
        font = pygame.font.Font(FONT_STYLE, 28)
        message_weapon = font.render(" You have DOUBLE DAMAGE for one hit! ", True, (255, 255, 255))
        icon = pygame.transform.scale(BULLET_DOUBLE, (60, 90))
        screen.blit(icon, (525, SCREEN_HEIGHT * 0.20))
        screen.blit(message_weapon, (SCREEN_WIDTH * 0.10, SCREEN_HEIGHT * 0.50))
        pygame.display.update()
        pygame.time.delay(1500)
    
    def draw_finish_power(self, screen):
        # Mostrar mensaje de finalización del poder
        font = pygame.font.Font(FONT_STYLE, 28)
        message_weapon = font.render(" You've used your power-up! ", True, (255, 255, 255))
        screen.blit(message_weapon, (SCREEN_WIDTH * 0.20, SCREEN_HEIGHT * 0.35))
        pygame.display.update()
        pygame.time.delay(1000)
        self.counter = 0

    def sound_shoot(self):
        # Reproducir sonido de disparo
        if self.current_spaceship == 0:
            self.shoot_sound.play()
        elif self.current_spaceship == 1:
            self.power_shoot_sound.play()

    def restart(self):
        # Reiniciar el juego
        self.hits.clear()
        self.counter = 0
