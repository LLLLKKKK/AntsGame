import pygame
from pygame.locals import *
import sys

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = (170, 170, 170)


class HighScore:

    def __init__(self):
        self.font = pygame.font.SysFont("Consolas Bold", 50)
        self.score_title = self.font.render("High Scores", True, WHITE)
        self.scores = []
        self.score_file = open('scores', 'a+')
        for line in self.score_file:
            self.scores.append(int(line))

        self.num_display = 5
        self.score_texts = []
        self.scores.sort(reverse=True)
        for index, score_ in enumerate(self.scores):
            if index > self.num_display:
                break
            self.score_texts.append(self.font.render(str(score_), True, WHITE))

    def __del__(self):
        self.score_file.close()

    def add_score(self, score):
        self.scores.append(score)
        self.scores.sort(reverse=True)
        self.score_file.write(str(score) + '\n')

        del self.score_texts[:]
        for index, score_ in enumerate(self.scores):
            if index > self.num_display:
                break
            color_now = None
            if score == score_:
                color_now = RED
            else:
                color_now = WHITE
            self.score_texts.append(self.font.render(str(score_), True, color_now))

    def update(self, screen, background, main):

        screen.blit(background, (0, 0))
        #screen.blit(self.logo, (50, 50))
        screen_height = screen.get_height()
        screen_width = screen.get_width()

        screen.blit(self.score_title, (screen_width / 2 - self.score_title.get_width() / 2, screen_height/6))

        for index, score_text in enumerate(self.score_texts):
            screen.blit(score_text, (screen_width / 2 - score_text.get_width() / 2, screen_height/6 + (score_text.get_height() + 20) * (index + 1)))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    main.set_state(main.States.Menu)
