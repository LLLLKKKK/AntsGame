import pygame, sys, random, ai, setting
from pygame.locals import *

random.seed()
pygame.init()

screen = pygame.display.set_mode(setting.SIZE)
pygame.display.set_caption('TERM PROJECT')

#######################################################################

wall = [] #[pos]

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

computer_ant_groupid = 0
player_ant_groupid = 1

pheromone_group = pygame.sprite.Group()
ant_groups = []
ant_groups.append(pygame.sprite.Group())
ant_groups.append(pygame.sprite.Group())
food_group = pygame.sprite.Group()
all_group = pygame.sprite.Group()

Pheromone.groups = pheromone_group, all_group
Food.groups = food_group, all_group

def get_enemy_groups(groupid):
    groups = []
    for gid, ant_group in enumerate(ant_groups):
        if gid != groupid:
            groups.append(ant_group)
    return groups
    
def spawn_ant(groupid):
    new_ant = Ant(groupid)
    new_ant.enemy_groups = ant_enemy_groups[groupid]
    ant_groups[groupid].add(new_ant)
    all_group.add(new_ant)

ant_enemy_groups = [0] * 2
ant_enemy_groups[player_ant_groupid] = get_enemy_groups(player_ant_groupid)
ant_enemy_groups[computer_ant_groupid] = get_enemy_groups(computer_ant_groupid)

spawn_ant(computer_ant_groupid)
spawn_ant(player_ant_groupid)

while True:
    
    milliseconds = clock.tick(FPS)
    seconds = milliseconds / 1000.0


    time_counter += 1
    if time_counter >= setting.TIME_SCALE:
        time_counter = 0
        
        posx = random.uniform(0, screen.get_width())
        posy = random.uniform(0, screen.get_height())
        Food((posx, posy))

    # Occur every frame
    # Handle input
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            Pheromone(pos)

    for groupid, ant_group in enumerate(ant_groups):
        killed_pheromone_dict = pheromone_eat_group = pygame.sprite.groupcollide(pheromone_group, ant_group, True, False)
        killed_food_dict = food_eat_group = pygame.sprite.groupcollide(food_group, ant_group, True, False)
        
        for foods in killed_food_dict.values():
            for food in foods:
                spawn_ant(groupid)

    pygame.sprite.groupcollide(ant_groups[0], ant_groups[1], True, True)

    all_group.clear(screen, background)
    all_group.update(seconds)
    all_group.draw(screen)

    pygame.display.flip()

    # print clock.get_fps()

    #pygame.display.update()
    #fpsClock.tick(setting.FPS)

