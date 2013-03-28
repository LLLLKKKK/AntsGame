import pygame, sys, random, ai, setting
from pygame.locals import *

random.seed()
pygame.init()

screen = pygame.display.set_mode(setting.SIZE)
pygame.display.set_caption('TERM PROJECT')

#######################################################################

wall = [] #[pos]

# In term of angle postive is counter clock wise. Negative is clockwise.
# 0 is upward (12 clock pos).
# For example 30 means 11 clock pos.
#########################################################################

#foods = game.Foods()
#player = game.Ants([90, 65])
#computer = game.Ants([10, 10])
#pheromones = game.Pheromones()

from game import Ant
from game import Pheromone
from game import Food

black = (0, 0, 0)

background = pygame.Surface((screen.get_width(), screen.get_height()))
background.fill(black)
background = background.convert()
screen.blit(background, (0, 0))

FPS = 60
time_counter = 0
clock = pygame.time.Clock()

pheromone_group = pygame.sprite.Group()
ant_group = pygame.sprite.Group()
food_group = pygame.sprite.Group()
all_group = pygame.sprite.Group()

Pheromone.groups = pheromone_group, all_group
Ant.groups = ant_group, all_group
Food.groups = food_group, all_group

Ant()

while True:
    
    milliseconds = clock.tick(FPS)
    seconds = milliseconds / 1000.0


    time_counter += 1
    if time_counter >= setting.TIME_SCALE:  # For every one second.
        time_counter = 0
        
        posx = random.uniform(0, screen.get_width())
        posy = random.uniform(0, screen.get_height())
        Food((posx, posy))
        #Ant()        
        # Spawn
        #player.spawn()
        #computer.spawn()

        #computer.spawn(enemy) # No computer AI yet.
        # Spawn food if not capped.
        
        #foods.spawn()
        
        # Find move target (where to move to)
        #ai.playerMove([player, computer, foods, pheromones, wall, [750, 550], [50, 50]])
        
        #pheromones.refresh()

    # Occur every frame
    # Handle input
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        #elif event.type == MOUSEMOTION:
        #    mousex, mousey == event.pos
        elif event.type == MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            Pheromone(pos)

    pheromone_eat_group = pygame.sprite.groupcollide(ant_group, pheromone_group, False, True)
    food_eat_group = pygame.sprite.groupcollide(ant_group, food_group, False, True)
    
    all_group.clear(screen, background)
    all_group.update(seconds)
    all_group.draw(screen)

    pygame.display.flip()

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
    
    #window.fill(black)
    #computer.draw(window, blue)
    #player.draw(window, green)

    #pygame.display.update()
    #fpsClock.tick(setting.FPS)

