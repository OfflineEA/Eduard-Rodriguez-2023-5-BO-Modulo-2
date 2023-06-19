import pygame

from game.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, GAMEOVER, FONT_STYLE

from game.components.spaceship import SpaceShip

from game.components.enemy import Enemy

class Game:
    def __init__(self):
        pygame.init()
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
        
    def run(self):
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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

            if self.enemy.counter_enemy >= 5:
                    if event.type == pygame.KEYDOWN:
                        self.spaceship.restart()
                        self.enemy.restart_enemy(520, 90)

    def update(self):
        self.spaceship.update()
        self.enemy.update_enemy()  

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        pygame.draw.rect(self.screen, (255, 255, 255), self.rect, 50)

        self.spaceship.shoot(self.screen)
        self.spaceship.draw(self.screen)
        self.enemy.shoot_enemy(self.screen,self.spaceship)
        self.enemy.draw_enemy(self.screen)

        if self.enemy.counter_enemy >= 5:
            self.game_over_screen()
            pygame.time.delay(1000)
        
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))
        image_height = image.get_height()
        self.screen.blit(image, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(image, (self.x_pos_bg, self.y_pos_bg - image_height))
        if self.y_pos_bg >= SCREEN_HEIGHT:
            self.screen.blit(image, (self.x_pos_bg, self.y_pos_bg - image_height))
            self.y_pos_bg = 0
        self.y_pos_bg += self.game_speed
    
    def game_over_screen(self):
        pygame.display.flip()
        font = pygame.font.Font(FONT_STYLE, 24)
        restart_text = font.render("Press any key to restart", True, (255, 255, 255))
        restart_text.get_rect()

        self.screen.fill((0, 0, 0))
        self.game_over = pygame.transform.scale(GAMEOVER, (520, 55))
        self.screen.blit(self.game_over, (290, SCREEN_HEIGHT * 0.40))
        self.screen.blit(restart_text, (SCREEN_WIDTH * 0.38, SCREEN_HEIGHT * 0.60))
        pygame.display.flip()
