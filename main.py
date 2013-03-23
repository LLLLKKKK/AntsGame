import pygame, sys, random, ai, setting, game
from pygame.locals import *

random.seed()
pygame.init()
fpsClock = pygame.time.Clock()

window = pygame.display.set_mode(setting.SIZE)
mousex, mousey = 0,0
pygame.display.set_caption('TERM PROJECT')

black = pygame.Color(0,0,0)
red = pygame.Color(255,0,0)
green = pygame.Color(0,255,0)
blue = pygame.Color(0,0,255)
white = pygame.Color(255,255,255)

#######################################################################

wall = [] #[pos]

# In term of angle postive is counter clock wise. Negative is clockwise.
# 0 is upward (12 clock pos).
# For example 30 means 11 clock pos.
#########################################################################

foods = game.Foods()
player = game.Ants([90, 65])
computer = game.Ants([10, 10])
pheromones = game.Pheromones()

timeCounter = 0
while True:
    
    # Game Logic
    timeCounter += 1
    # Occur every few frame
    if timeCounter >= setting.TIME_SCALE:  # For every one second.
        timeCounter = 0        
        # Spawn
        player.spawn()
        computer.spawn()

        #computer.spawn(enemy) # No computer AI yet.
        # Spawn food if not capped.
        
        foods.spawn()
        
        # Find move target (where to move to)
        ai.playerMove([player, computer, foods, pheromones, wall, [750, 550], [50, 50]])
        
        pheromones.refresh()

    # Occur every frame
    # Handle input
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEMOTION:
            mousex, mousey == event.pos
        elif event.type == MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            pheromones.spawn()

    ###############
    # Display
    # TEMP now all ant are just dots.
    # Use the old data and new data.
    # The index is the same for the new data and old data.
    # If an ant is killed off then the new Data will have the pos as -1,-1
    # The whole game is a made up of 8 by 8 grids.
    # for example if a ant at 0, 0 means the center of the image of ant should be at 4,4.
    # To convert should just be [x,y] => [x*8+4, y*8+4]
    #############
    
    window.fill(black)
    computer.draw(window, blue)
    player.draw(window, green)

    pygame.display.update()
    fpsClock.tick(setting.FPS)

