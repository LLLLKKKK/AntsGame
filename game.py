import sys, os
from sprites import *
from pygame.locals import *
import pygame.mixer


class Game:

    def __init__(self):

        self.computer_ant_groupid = 1
        self.player_ant_groupid = 0

        self.pheromone_group = pygame.sprite.Group()
        self.ant_groups = []
        self.ant_groups.append(pygame.sprite.Group())
        self.ant_groups.append(pygame.sprite.Group())
        self.food_group = pygame.sprite.Group()
        self.all_group = pygame.sprite.Group()
        self.cursor_group = pygame.sprite.Group()

        Pheromone.groups = self.pheromone_group, self.all_group
        Food.groups = self.food_group, self.all_group
        Cursor.groups = self.cursor_group

        self.show_range = False

        self.ant_enemy_groups = [0] * 2
        self.ant_enemy_groups[self.player_ant_groupid] = self.get_enemy_groups(self.player_ant_groupid)
        self.ant_enemy_groups[self.computer_ant_groupid] = self.get_enemy_groups(self.computer_ant_groupid)

        self.time_counter = 0
        self.score = 0

        self.font = pygame.font.SysFont("Consolas", 30)

        self.explosion_sound = pygame.mixer.Sound(os.path.join("sounds", "explosion.wav"))
        self.eat_sound = pygame.mixer.Sound(os.path.join("sounds", "eat.wav"))

        self.cursor = Cursor()

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

    def reset(self):
        # clear all groups
        self.pheromone_group.empty()
        self.food_group.empty()
        for ant_group in self.ant_groups:
            ant_group.empty()
        self.all_group.empty()

        self.time_counter = 0
        self.score = 0

        # spawn new ants
        self.spawn_ant(self.computer_ant_groupid)
        self.spawn_ant(self.player_ant_groupid)
        self.clock = pygame.time.Clock()

    def stop(self, main):
        main.highscore.add_score(self.score)
        main.set_state(main.States.HighScore)

    def generate_food(self, screen):
        self.time_counter += 1
        if self.time_counter >= setting.TIME_SCALE:
            self.time_counter = 0

            posx = random.uniform(0, screen.get_width())
            posy = random.uniform(0, screen.get_height())
            Food((posx, posy))

    def update(self, screen, background, main):

        screen.blit(background, (0, 0))
        screen_height = screen.get_height()
        screen_width = screen.get_width()

        milliseconds = self.clock.tick(60)
        seconds = milliseconds / 1000.0

        self.cursor.rect.center = pygame.mouse.get_pos()
        if self.show_range:
            self.cursor_group.draw(screen)

        self.generate_food(screen)

        for groupid, ant_group in enumerate(self.ant_groups):
            pheromone_collide_func = lambda s1, s2: s1.pheromone_rect.colliderect(s2.rect)
            killed_pheromone_dict = pygame.sprite.groupcollide(self.pheromone_group, ant_group, True, False, pheromone_collide_func)
            killed_food_dict = pygame.sprite.groupcollide(self.food_group, ant_group, True, False)

            if groupid == self.player_ant_groupid:
                self.score += len(killed_food_dict) * 20
            self.score -= len(killed_pheromone_dict) * 50

            for foods in killed_food_dict.values():
                for food in foods:
                    self.eat_sound.play()
                    self.spawn_ant(groupid)

        killed_ant_dict = pygame.sprite.groupcollide(self.ant_groups[0], self.ant_groups[1], True, True)
        for ant in killed_ant_dict:
            self.eat_sound.stop()
            self.explosion_sound.play()

        self.all_group.clear(screen, background)
        self.all_group.update(seconds)
        self.all_group.draw(screen)

        score_text = self.font.render("Score: " + str(self.score), True, (255, 255, 255))
        screen.blit(score_text, (screen_width - score_text.get_width() - 10, screen_height - score_text.get_height() - 10))

        ############################################
        # End game when one group is eliminated
        if not self.ant_groups[0]:
            # No player Ant left
            self.stop(main)
        if not self.ant_groups[1]:
            # No computer ant left
            self.stop(main)
        #############################################

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                mouse_pressed = pygame.mouse.get_pressed()
                pos = pygame.mouse.get_pos()
                if mouse_pressed[0]:
                    Pheromone(pos)
                elif mouse_pressed[2]:
                    self.show_range = not self.show_range
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    self.stop(main)
