import pygame

from game.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, GAMEOVER, FONT_STYLE

from game.components.spaceship import SpaceShip

from game.components.enemy import Enemy

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False  
        self.game_speed = 10
        self.x_pos_bg = 0
        self.y_pos_bg = 0
        self.enemy = Enemy(520, 90)
        self.spaceship = SpaceShip()
        self.rect = pygame.Rect(0, 570, 1100, 80)
        self.rounds = 1
        pygame.mixer.music.load("Eduard-Rodriguez-2023-5-BO-Modulo-2/game/assets/Songs/SongLoop.mp3")
        self.game_over_sound = pygame.mixer.Sound("Eduard-Rodriguez-2023-5-BO-Modulo-2/game/assets/Songs/Dead.wav")
        pygame.mixer.music.set_volume(0.2)
        self.game_over_sound.set_volume(0.1)
    
    def run(self):
        pygame.mixer.music.play(-1)
        self.playing = True
        while self.playing: 
            self.handle_events()
            self.update()
            self.draw()
        else:
            print("Something ocurred to quit the game!!!")
        pygame.display.quit()
        pygame.quit()

    def handle_events(self):
        # Maneja los eventos del juego, como salir del juego o reiniciar después de perder
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                self.playing = False

            if self.enemy.counter_enemy == 5:
                pygame.mixer.music.pause()
                self.game_over_sound.play()
                if event.type == pygame.KEYDOWN:
                    self.rounds = self.rounds + 1
                    self.spaceship.restart()
                    self.enemy.restart(520, 90)
                    pygame.mixer.music.unpause()

    def update(self):
        # Actualiza la lógica del juego
        self.spaceship.update()
        self.enemy.update_enemy()  

    def draw(self):
        # Dibuja los elementos del juego en la pantalla
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        pygame.draw.rect(self.screen, (255, 255, 255), self.rect, 50)

        self.spaceship.shoot(self.screen, self.enemy)
        self.spaceship.draw(self.screen)
        self.enemy.shoot_enemy(self.screen,self.spaceship)
        self.enemy.draw_enemy(self.screen)

        if self.enemy.counter_enemy >= 5:
            self.draw_game_over()
            pygame.time.delay(1000)
        
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        # Dibuja el fondo en movimiento del juego
        image = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))
        image_height = image.get_height()
        self.screen.blit(image, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(image, (self.x_pos_bg, self.y_pos_bg - image_height))
        if self.y_pos_bg >= SCREEN_HEIGHT:
            self.screen.blit(image, (self.x_pos_bg, self.y_pos_bg - image_height))
            self.y_pos_bg = 0
        self.y_pos_bg += self.game_speed
    
    def draw_game_over(self):
        # Dibuja la pantalla de Game Over
        font = pygame.font.Font(FONT_STYLE, 24)
        self.game_over = pygame.transform.scale(GAMEOVER, (520, 55))
        restart_text = font.render("Press any key to restart", True, (255, 255, 255))
        restart_text.get_rect()

        highscore_text = font.render(f"Your record is: {len(self.spaceship.hits)}", True, (255, 255, 255))
        highscore_text.get_rect()

        round_text = font.render(f"You are in the round: {self.rounds}", True, (255, 255, 255))
        round_text.get_rect()

        self.screen.fill((0, 0, 0))
        self.screen.blit(self.game_over, (290, SCREEN_HEIGHT * 0.40))
        self.screen.blit(restart_text, (SCREEN_WIDTH * 0.28, SCREEN_HEIGHT * 0.60))
        self.screen.blit(highscore_text, (SCREEN_WIDTH * 0.28, SCREEN_HEIGHT * 0.65))
        self.screen.blit(round_text, (SCREEN_WIDTH * 0.28, SCREEN_HEIGHT * 0.70))
        pygame.display.flip()
