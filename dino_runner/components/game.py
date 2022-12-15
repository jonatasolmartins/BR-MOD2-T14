import pygame

from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, DEFAULT_TYPE
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import Obstacle_Manager
from dino_runner.utils.text_utils import draw_message_component

FONT_COLOR = (0,0,0)
FONT_SIZE = 22
FONT_STYLE = "freesansbold.ttf"

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.running = False
        self.score = 0
        self.death_count = 0
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.player = Dinosaur()
        self.obstacle_manager = Obstacle_Manager()
        #powerupmanager

    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()
        #desliga o jogo
        pygame.display.quit()
        #fecha a janela
        pygame.quit()
               

    def run(self):
        # Game loop: events - update - draw
        self.playing = True
       
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.update_score()
        self.obstacle_manager.update(self)

    def update_score(self):
        self.score += 1
        self.update_game_speed()

    def update_game_speed(self):
        if self.score % 100 == 0:
            self.game_speed += 1

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255)) # "#FFFFFF"
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.draw_score()
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def draw_score(self):
        self.draw_message_component(
            f"Score: {self.score}",self.screen, pos_y_center = 50,pos_x_center=SCREEN_WIDTH - 140)

    def draw_message_component(
        self, message, screen,
        font_color= FONT_COLOR,
        font_size = FONT_SIZE,
        font_style = FONT_STYLE,
        pos_y_center = SCREEN_HEIGHT // 2,
        pos_x_center = SCREEN_WIDTH // 2):

        font = pygame.font.Font(font_style, font_size)
        text = font.render(message, True, font_color)
        text_rect = text.get_rect()
        text_rect.x = pos_x_center
        text_rect.y = pos_y_center
        screen.blit(text, text_rect)

    def handle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.run()

    def show_menu(self):
        
        self.screen.fill((255, 255, 255))
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2

        if self.death_count == 0:
           draw_message_component("Press any key to start", self.screen)
        else:
            draw_message_component("Press any key to restart", self.screen, pos_y_center=half_screen_height + 140)
            draw_message_component(
                f"Your Score: {self.score}",
                self.screen,
                pos_y_center=half_screen_height - 150
            )            
            draw_message_component(
                f"Death count: {self.death_count}",
                self.screen,
                pos_y_center=half_screen_height - 100
            )
            self.screen.blit(ICON, (half_screen_width - 40, half_screen_height - 30))

        pygame.display.flip()
        self.handle_events_on_menu()


