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
food = [] #[pos]
pheromone = [] # [pos]
pheromoneTime = []
wall = [] #[pos]
ant = [] #player's ant [pos, angle]
enemy = [] #computer's ant [pos, angle]
# In term of angle postive is counter clock wise. Negative is clockwise.
# 0 is upward (12 clock pos).
# For example 30 means 11 clock pos.
#########################################################################

foodSpawn = game.SpawnFood()
player = game.SpawnAnt([750, 550])
computer = game.SpawnAnt([50, 50])

timeCounter = 0
while True:
    ####################################### OLD DATA
    oldFood = food
    oldPheromone = pheromone
    oldAnt = ant
    oldEnemy = enemy
    #######################################
    
    # Game Logic
    timeCounter += 1
    # Occur every few frame
    if timeCounter >= setting.TIME_SCALE:  # For every one second.
        timeCounter = 0        
        # Spawn
        player.spawn(ant)
        #computer.spawn(enemy) # No computer AI yet.
        # Spawn food if not capped.
        if(len(food) < setting.MAX_FOOD):
            foodSpawn.spawn(food)
        
        # Find move target (where to move to)
        ai.playerMove([ant, enemy, food, pheromone, wall, [750, 550], [50, 50]])
        
        # Pheromone lifetime
        for i, x in enumerate(pheromoneTime):
            pheromoneTime[i] -= 1
            # remove pheromone with 0 lifetime
            if(pheromoneTime[i] <= 0):
                pheromone.pop(i)
                pheromoneTime.pop(i)

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
            temp = [pos[0], pos[1]]
            # Remove first pheromone if too many
            if(len(pheromone) > setting.MAX_PHEROMONE):
                pheromone.pop(0)
            pheromone.append(temp)
            pheromoneTime.append(setting.PHEROMONE_LIFETIME)

    
    # Display
    # TEMP now all ant are just dots.
    # Use the old data and new data.
    # The index is the same for the new data and old data.
    # If an ant is killed off then the new Data will have the pos as -1,-1
    window.fill(black)
    for pos in ant:
        pygame.draw.circle(window, blue, pos, 4)
    for pos in food:
        pygame.draw.circle(window, white, pos, 2)
    for pos in pheromone:
        print pos
        pygame.draw.circle(window, green, pos, 2)
    
            
    pygame.display.update()
    fpsClock.tick(setting.FPS)
