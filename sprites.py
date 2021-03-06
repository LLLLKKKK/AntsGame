import random
import os
import math
import pygame
from pygame.locals import *
from configs import *

random.seed()


# def create_circle_image(diameter, color):
#     image = pygame.Surface((diameter * 2, diameter * 2))
#     image.set_colorkey((0, 0, 0))
#     pygame.draw.circle(image, color, (diameter, diameter), 4)
#     image = image.convert_alpha()
#     return image


class Ant(pygame.sprite.Sprite):

    # static class variables
    # image setup

    images = []

    ant_image = pygame.image.load(os.path.join("images", "green_ant.bmp")).convert()
    ant_image.set_colorkey(ant_image.get_at((0, 0)))
    images.append(ant_image)

    ant_image = pygame.image.load(os.path.join("images", "blue_ant.bmp")).convert()
    ant_image.set_colorkey(ant_image.get_at((0, 0)))
    images.append(ant_image)

    hives = []
    hives.append((10, 20))
    hives.append((770, 570))

    angels = []
    angels.append(math.pi/4)
    angels.append(-math.pi/4)

    spread_length = 20.0
    speed = 100.0
    food_vision = 100
    AI_food_vision = 300
    enemy_vision = 150
    pheromone_vision = 200

    # code for each individual class instances
    def __init__(self, groupid):
        pygame.sprite.Sprite.__init__(self)

        self.image = Ant.images[groupid]

        self.rect = self.image.get_rect()
        self.rect.center = Ant.hives[groupid]
        self.radius = 100
        self.angle = Ant.angels[groupid]

        self.spread_length = Ant.spread_length
        self.speed = Ant.speed

        self.centerx = self.rect.centerx
        self.centery = self.rect.centery
        self.groupid = groupid

        self.rotate()

    def distance(self, obj):
        center1 = self.get_center()
        center2 = obj.get_center()
        return math.hypot(center1[0] - center2[0],
                          center1[1] - center2[1])

    def closest_object(self, object_group):
        if len(object_group) > 0:
            it = iter(object_group)
            obj = it.next()
            for i in it:
                if (self.distance(i) < self.distance(obj)):
                    obj = i
            return obj
        else:
            pass

    def turn_to(self, obj):
        center1 = self.get_center()
        center2 = obj.get_center()

        dist_x = center2[0] - center1[0]
        dist_y = center2[1] - center1[1]

        if dist_x != 0:
            if dist_x > 0:
                self.angle = math.atan(dist_y * 1.0 / dist_x)
            else:
                self.angle = math.pi + math.atan(dist_y * 1.0 / dist_x)
        else:
            if dist_y > 0:
                self.angle = -math.pi / 2.0
            else:
                self.angle = math.pi / 2.0

    def update(self, seconds):

        move_length = seconds * self.speed
        is_attracted = False

        ##############################################
        # Player AI
        if(self.groupid == 0):
            closest_pheromone = self.closest_object(Pheromone.groups[0])
            if (self.groupid == 0 and not (closest_pheromone is None)) and self.distance(closest_pheromone) < Ant.pheromone_vision:
                self.turn_to(closest_pheromone)
                is_attracted = True
            else:
                closest_enemy = self.closest_object(self.enemy_groups[0])
                if (not (closest_enemy is None)) and self.distance(closest_enemy) < Ant.enemy_vision:
                    self.turn_to(closest_enemy)
                    is_attracted = True
                else:
                    closest_food = self.closest_object(Food.groups[0])
                    if (not (closest_food is None)) and self.distance(closest_food) < Ant.food_vision:
                        self.turn_to(closest_food)
                        is_attracted = True
        # Enemy AI
        else:
            closest_enemy = self.closest_object(self.enemy_groups[0])
            if (not (closest_enemy is None)) and self.distance(closest_enemy) < Ant.enemy_vision:
                self.turn_to(closest_enemy)
                is_attracted = True
            else:
                closest_food = self.closest_object(Food.groups[0])
                if (not (closest_food is None)) and self.distance(closest_food) < Ant.AI_food_vision:
                    self.turn_to(closest_food)
                    is_attracted = True
        ###############################################

        if not is_attracted:
            self.spread_length -= move_length
            if self.spread_length < 0:
                self.angle += random.uniform(-math.pi / 4, math.pi / 4)
                self.spread_length = Ant.spread_length
        else:
            self.spread_length = Ant.spread_length

        self.rotate()
        self.move(move_length)

    def move(self, move_length):

        self.centerx += move_length * math.cos(self.angle)
        self.centery += move_length * math.sin(self.angle)

        if (self.centerx < 0):
            self.centerx = -self.centerx
            self.angle = math.pi + self.angle

        if (self.centerx > screen_width):
            self.centerx = 2 * screen_width - self.centerx
            self.angle = math.pi + self.angle

        if (self.centery < 0):
            self.centery = -self.centery
            self.angle = math.pi + self.angle

        if (self.centery > screen_height):
            self.centery = 2 * screen_height - self.centery
            self.angle = math.pi + self.angle

        self.rect.centerx = round(self.centerx, 0)
        self.rect.centery = round(self.centery, 0)

    def rotate(self):
        old_self_rect_center = self.rect.center
        old_image_rect_center = self.image.get_rect().center
        rotated_image = pygame.transform.rotate(Ant.images[self.groupid], -self.angle / math.pi * 180)
        new_image_rect_center = rotated_image.get_rect().center
        self.rect.center = (old_self_rect_center[0] + (old_image_rect_center[0] - new_image_rect_center[0]), old_self_rect_center[1] + (old_image_rect_center[1] - new_image_rect_center[1]))

        self.image = rotated_image

    def get_center(self):
        return self.rect.center


class Pheromone(pygame.sprite.Sprite):
    # static class variables
    # image setup

    image = pygame.Surface((Ant.pheromone_vision * 2, Ant.pheromone_vision * 2))
    image.set_colorkey((0, 0, 0))

    pygame.draw.circle(image, (255, 0, 255), (Ant.pheromone_vision, Ant.pheromone_vision), 4)
    pygame.draw.circle(image, (255, 0, 255), (Ant.pheromone_vision, Ant.pheromone_vision), Ant.pheromone_vision, 2)

    # code for each individual class instances
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = Pheromone.image
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.pheromone_rect = pygame.Rect(pos, (4, 4))
        self.radius = 4
        self.live = 10.0

    def update(self, seconds):
        self.live -= seconds
        if self.live < 0:
            self.kill()

    def get_center(self):
        return self.rect.center


class Food(pygame.sprite.Sprite):

    # static class variables
    # image setup
    image = pygame.Surface((8, 8))
    image.set_colorkey((0, 0, 0))
    pygame.draw.circle(image, (255, 0, 0), (4, 4), 4)
    image = image.convert_alpha()

    # code for each individual class instances
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = Food.image
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.radius = 4

    def update(self, seconds):
        pass

    def get_center(self):
        return self.rect.center


class Cursor(pygame.sprite.Sprite):

    image = pygame.Surface((Ant.pheromone_vision * 2, Ant.pheromone_vision * 2))
    image.set_colorkey((0, 0, 0))

    pygame.draw.circle(image, (255, 0, 255), (Ant.pheromone_vision, Ant.pheromone_vision), Ant.pheromone_vision, 1)
    image = image.convert_alpha()

    # code for each individual class instances
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = Cursor.image
        self.rect = self.image.get_rect()

    def update(self, seconds):
        pass
