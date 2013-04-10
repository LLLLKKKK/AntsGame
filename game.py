import sys
from sprites import *

class Game:

    def __init__(self):

        self.computer_ant_groupid = 0
        self.player_ant_groupid = 1

        self.pheromone_group = pygame.sprite.Group()
        self.ant_groups = []
        self.ant_groups.append(pygame.sprite.Group())
        self.ant_groups.append(pygame.sprite.Group())
        self.food_group = pygame.sprite.Group()
        self.all_group = pygame.sprite.Group()

        Pheromone.groups = self.pheromone_group, self.all_group
        Food.groups = self.food_group, self.all_group

        self.ant_enemy_groups = [0] * 2
        self.ant_enemy_groups[self.player_ant_groupid] = self.get_enemy_groups(self.player_ant_groupid)
        self.ant_enemy_groups[self.computer_ant_groupid] = self.get_enemy_groups(self.computer_ant_groupid)

        self.spawn_ant(self.computer_ant_groupid)
        self.spawn_ant(self.player_ant_groupid)

        self.time_counter = 0
        self.clock = pygame.time.Clock()

    def get_enemy_groups(self, groupid):
        groups = []
        for gid, ant_group in enumerate(self.ant_groups):
            if gid != groupid:
                groups.append(ant_group)
        return groups
        
    def spawn_ant(self, groupid):
        new_ant = Ant(groupid)
        new_ant.enemy_groups = self.ant_enemy_groups[groupid]
        self.ant_groups[groupid].add(new_ant)
        self.all_group.add(new_ant)

    def update(self, screen, background):

        milliseconds = self.clock.tick(60)
        seconds = milliseconds / 1000.0
        
        self.time_counter += 1
        if self.time_counter >= setting.TIME_SCALE:
            self.time_counter = 0
            
            posx = random.uniform(0, screen.get_width())
            posy = random.uniform(0, screen.get_height())
            Food((posx, posy))
        
        for groupid, ant_group in enumerate(self.ant_groups):
            killed_pheromone_dict = pheromone_eat_group = pygame.sprite.groupcollide(self.pheromone_group, ant_group, True, False)
            killed_food_dict = food_eat_group = pygame.sprite.groupcollide(self.food_group, ant_group, True, False)
            
            for foods in killed_food_dict.values():
                for food in foods:
                    self.spawn_ant(groupid)

        pygame.sprite.groupcollide(self.ant_groups[0], self.ant_groups[1], True, True)

        self.all_group.clear(screen, background)
        self.all_group.update(seconds)
        self.all_group.draw(screen)
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                Pheromone(pos)

