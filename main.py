import pygame
from pygame.locals import *

class Main:

    class States:
        Menu, Game = range(2)

    def __init__(self):

        pygame.init()
        pygame.display.set_caption('TERM PROJECT')

        self.screen = pygame.display.set_mode((800, 600))
        self.background = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        self.background.fill((0, 0, 0))
        
        self.now_state = Main.States.Game
        
        import game
        self.game = game.Game()
        
        self.start()

    def start(self):

        while True:
            #if self.now_state == Main.States.Menu:
            #    pass
            #elif self.now_state == Main.States.Game:
            self.game.update(self.screen, self.background)
            

Main()
