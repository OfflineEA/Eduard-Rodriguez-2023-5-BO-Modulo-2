import pygame
import random

from pygame.sprite import Sprite
from game.components.bullet import Bullet

from game.utils.constants import ENEMY_2, SCREEN_WIDTH, SCREEN_HEIGHT, BULLET_ENEMY, FONT_STYLE

class Enemy(Sprite):
    def __init__(self, position_x, position_y):
        super().__init__()
        pygame.mixer.init()
        
        # Configuración de la imagen y posición del enemigo
        self.image_size_enemy = (60, 90)
        self.ship_enemy = pygame.transform.scale(ENEMY_2, self.image_size_enemy)
        self.image_rect_enemy = self.ship_enemy.get_rect()
        self.image_rect_enemy.x = position_x      # Recomendado: 520
        self.image_rect_enemy.y = position_y      # Recomendado: 90
        
        # Configuración del movimiento del enemigo
        self.movement_enemy = 10
        self.direction_enemy = 1
        
        # Configuración de la bala del enemigo
        self.bullet_enemy = Bullet(self.image_rect_enemy.center, BULLET_ENEMY)
        
        # Variables para llevar registro de los golpes y daño recibido
        self.hits_enemy = []
        self.counter_enemy = 0
        
        # Configuración de los sonidos
        self.shoot_sound = pygame.mixer.Sound("Eduard-Rodriguez-2023-5-BO-Modulo-2/game/assets/Songs/Shoot_Enemy.wav")
        self.sound_damage = pygame.mixer.Sound("Eduard-Rodriguez-2023-5-BO-Modulo-2/game/assets/Songs/Received_Damage.wav")
        self.shoot_sound.set_volume(0.2)
        self.sound_damage.set_volume(0.2)
    
    def update_enemy(self):
        # Actualizar movimiento del enemigo
        self.move_enemy()
    
    def move_enemy(self):
        # Mover el enemigo horizontalmente y actualizar posición de la bala
        self.image_rect_enemy.x += self.movement_enemy * self.direction_enemy
        self.bullet_enemy.bullet_rect.x = self.image_rect_enemy.x + 18
        
        # Cambiar dirección cuando alcanza los límites de la pantalla
        if self.image_rect_enemy.x <= 0 or self.image_rect_enemy.x + self.image_size_enemy[0] > SCREEN_WIDTH:
            self.direction_enemy *= -1
            self.image_rect_enemy.x += self.direction_enemy
            self.bullet_enemy.bullet_rect.x = self.image_rect_enemy.x

    def draw_enemy(self, screen):
        # Dibujar enemigo en la pantalla y mostrar el estado del enemigo
        screen.blit(self.ship_enemy, self.image_rect_enemy)
        self.draw_status_enemy(screen)
        
    def shoot_enemy(self, screen, spaceship):
        # Realizar disparo del enemigo
        self.current_time = pygame.time.get_ticks()
        time_between_shots = random.randrange(700, 1000, 100)
        
        # Comprobar si ha pasado suficiente tiempo para disparar
        if self.current_time - self.enemy_timer > time_between_shots:
            self.shoot_sound.play()
            while True:
                self.bullet_enemy.bullet_rect.y += self.movement_enemy
                self.bullet_enemy.draw(screen)
                
                # Comprobar colisión con la nave espacial
                if self.bullet_enemy.bullet_rect.colliderect(spaceship.image_rect):
                    self.shoot_sound.stop()
                    self.hit = 1
                    self.hits_enemy.append(self.hit)
                    self.draw_hit_enemy(screen)
                    self.bullet_enemy.bullet_rect.y = self.image_rect_enemy.y + 20
                    break
                
                # Comprobar si la bala ha salido de la pantalla
                if self.bullet_enemy.bullet_rect.y >= SCREEN_HEIGHT:
                    self.shoot_sound.stop()
                    self.bullet_enemy.update()
                    self.bullet_enemy.bullet_rect.y = self.image_rect_enemy.y + 20
                    self.enemy_timer = self.current_time
                return False
    
    def draw_hit_enemy(self, screen):
        # Mostrar mensaje de impacto del enemigo en la nave espacial
        self.sound_damage.play()
        font = pygame.font.Font(FONT_STYLE, 28)
        text = font.render(" The enemy has hit you! ", True, (255, 255, 255))
        screen.blit(text, (SCREEN_WIDTH * 0.25, SCREEN_HEIGHT * 0.40))
        pygame.display.update()
        pygame.time.delay(2000)

    def draw_status_enemy(self, screen):
        # Mostrar el estado del enemigo (daño recibido)
        font = pygame.font.Font(FONT_STYLE, 22)
        self.counter_enemy = len(self.hits_enemy)
        text = f" Damage received: {self.counter_enemy} "
        message = font.render(text, True, (0, 0, 0))
        message.get_rect()
        screen.blit(message, (SCREEN_WIDTH * 0.68, SCREEN_HEIGHT * 0.96))

    def restart(self, position_x, position_y):
        # Reiniciar los valores del enemigo
        self.counter_enemy = 0
        self.hits_enemy.clear()
        self.image_rect_enemy.x = position_x      
        self.image_rect_enemy.y = position_y
