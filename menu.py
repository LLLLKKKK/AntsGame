import pygame
from pygame.locals import *
import sys

WHITE = (255, 255, 255)
GRAY = (170, 170, 170)


class Menu:

    class MenuItem:
        NewGame, HighScore, Quit = range(3)
        First = 0
        Last = 2

    def __init__(self):
        #self.logo = pygame.image.load(os.path.join("graphics", "logo.png")).convert()
        #self.logo = pygame.transform.scale(self.logo, (int(3.5*screen_width/4), screen_height/4))
        #self.logo.set_colorkey(self.logo.get_at((0, 0)))

        self.now_item = Menu.MenuItem.NewGame

        font = pygame.font.SysFont("Consolas", 30)
        self.newgame_o = font.render("New Game", True, WHITE)
        self.newgame_f = font.render("New Game", True, GRAY)
        self.quit_o = font.render("Quit", True, WHITE)
        self.quit_f = font.render("Quit", True, GRAY)
        self.highscores_o = font.render("High Scores", True, WHITE)
        self.highscores_f = font.render("High Scores", True, GRAY)

        self.now_item = 0

    def update(self, screen, background, main):
        #t = pygame.time.get_ticks()
        screen.blit(background, (0, 0))
        #screen.blit(self.logo, (50, 50))
        screen_height = screen.get_height()
        screen_width = screen.get_width()

        if self.now_item == Menu.MenuItem.NewGame:
            screen.blit(self.newgame_o, (screen_width/2 - self.newgame_o.get_width()/2, 2*screen_height/3))
        else:
            screen.blit(self.newgame_f, (screen_width/2 - self.newgame_f.get_width()/2, 2*screen_height/3))

        if self.now_item == Menu.MenuItem.HighScore:
            screen.blit(self.highscores_o, (screen_width/2 - self.highscores_f.get_width()/2, 2*screen_height/3 + 35))
        else:
            screen.blit(self.highscores_f, (screen_width/2 - self.highscores_f.get_width()/2, 2*screen_height/3 + 35))

        if self.now_item == Menu.MenuItem.Quit:
            screen.blit(self.quit_o, (screen_width/2 - self.quit_o.get_width()/2, 2*screen_height/3 + 70))
        else:
            screen.blit(self.quit_f, (screen_width/2 - self.quit_o.get_width()/2, 2*screen_height/3 + 70))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_UP and self.now_item != Menu.MenuItem.First:
                    self.now_item -= 1
                elif event.key == K_DOWN and self.now_item != Menu.MenuItem.Last:
                    self.now_item += 1
                elif event.key == K_SPACE:
                    if self.now_item == Menu.MenuItem.NewGame:
                        main.set_state(main.States.Game)
                    elif self.now_item == Menu.MenuItem.HighScore:
                        main.set_state(main.States.HighScore)
                    elif self.now_item == Menu.MenuItem.Quit:
                        pygame.quit()
                        sys.exit()
