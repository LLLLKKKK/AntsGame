#!/usr/bin/env python

import os
import pygame
from pygame.locals import *
import pygame.mixer


class Main:

    class States:
        Menu, Game, HighScore = range(3)

    def __init__(self):

        pygame.init()
        pygame.display.set_caption('Ants')

        self.screen = pygame.display.set_mode((800, 600))
        self.background = pygame.image.load(os.path.join("images", "soil.jpg"))
        # self.background = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        # self.background.fill((0, 0, 0))

        self.now_state = Main.States.Menu

        import game
        import menu
        import highscore

        self.game = game.Game()
        self.menu = menu.Menu()
        self.highscore = highscore.HighScore()

        self.soundtrack = pygame.mixer.Sound(os.path.join("sounds", "soundtrack.wav"))

        self.start()

    def start(self):

        self.soundtrack.play(-1)

        while True:
            if self.now_state == Main.States.Menu:
                self.menu.update(self.screen, self.background, self)
            elif self.now_state == Main.States.Game:
                self.game.update(self.screen, self.background, self)
            elif self.now_state == Main.States.HighScore:
                self.highscore.update(self.screen, self.background, self)

            pygame.display.update()

    def set_state(self, new_state):
        self.now_state = new_state
        if new_state == Main.States.Game:
            self.game.reset()

if __name__ == "__main__":
    Main()
