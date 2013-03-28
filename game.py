import setting, random, pygame, math
from pygame.locals import *

random.seed()

def dist(obj1, obj2):
    center1 = obj1.get_center();
    center2 = obj2.get_center();
    return math.hypot(center1[0] - center2[0], 
                      center1[1] - center2[1])

def closest_object(ant, object_group):
    if len(object_group) > 0:
        it = iter(object_group)
        obj = it.next()
        for i in it:
            if (dist(ant, i) < dist(ant, obj)):
                obj = i
        return obj
    else:
        pass

def object_turn_to(obj1, obj2):
    center1 = obj1.get_center();
    center2 = obj2.get_center();
    
    dist_x = center2[0] - center1[0]
    dist_y = center2[1] - center1[1]

    if dist_x != 0:
        if dist_x > 0:
            obj1.angle = math.atan(dist_y * 1.0 / dist_x)
        else:
            obj1.angle = math.pi + math.atan(dist_y * 1.0 / dist_x)
    else:
        if dist_y > 0:
            obj1.angle = -math.pi / 2.0
        else:
            obj1.angle = math.pi / 2.0

class Ant(pygame.sprite.Sprite):
    
    # static class variables
    # image setup
    image = pygame.Surface((8, 8))
    image.set_colorkey((0, 0, 0))
    pygame.draw.circle(image, (255, 255, 0), (4, 4), 4)
    image = image.convert_alpha()

    food_vision = 100
    pheromone_vision = 200

    # code for each individual class instances
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = Ant.image
        self.rect = self.image.get_rect()
        self.rect.center = (10, 10)
        self.radius = 100
        self.angle = math.pi / 4

    def update(self, seconds):

        closest_pheromone =  closest_object(self, Pheromone.groups[0])
        if (not (closest_pheromone is None)) and dist(closest_pheromone, self) < Ant.pheromone_vision:
            object_turn_to(self, closest_pheromone)
        else:
            closest_food =  closest_object(self, Food.groups[0])
            if (not (closest_food is None)) and dist(closest_food, self) < Ant.food_vision:
                object_turn_to(self, closest_food)

        self.rect.centerx += round(seconds * 50.0 * math.cos(self.angle), 0)
        self.rect.centery += round(seconds * 50.0 * math.sin(self.angle), 0)

        if (self.rect.centerx < 0):
            self.rect.centerx = 0
            
        if (self.rect.centery < 0):
            self.rect.centery = 0

    def rotate(self, angle):
        old_self_rect_center = self.rect.center
        old_image_rect_center = self.image.get_rect().center
        rotated_image =  pygame.transform.rotate(Ant.image, self.angle)
        new_image_rect_center = rotated_image.get_rect().center
        self.rect.center = (old_self_rect_center[0] + (old_image_rect_center[0] - new_image_rect_center[0]), old_self_rect_center[1] + (old_image_rect_center[1] - new_image_rect_center[1]))

        self.image = rotated_image

    def get_center(self):
        return self.rect.center


class Pheromone(pygame.sprite.Sprite):
    
    # static class variables
    # image setup
    image = pygame.Surface((8, 8))
    image.set_colorkey((0, 0, 0))
    pygame.draw.circle(image, (255, 0, 255), (4, 4), 4)
    image = image.convert_alpha()


    # code for each individual class instances
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = Pheromone.image
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.radius = 100
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
    pygame.draw.circle(image, (0, 255, 0), (4, 4), 4)
    image = image.convert_alpha()


    # code for each individual class instances
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = Food.image
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.radius = 100

    def update(self, seconds):
        pass

    def get_center(self):
        return self.rect.center        