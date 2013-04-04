import setting, random, pygame, math
from pygame.locals import *
from setting import screen_width, screen_height

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

def create_circle_image(diameter, color):
    image = pygame.Surface((diameter * 2, diameter * 2))
    image.set_colorkey((0, 0, 0))
    pygame.draw.circle(image, color, (diameter, diameter), 4)    
    image = image.convert_alpha()
    return image

class Ant(pygame.sprite.Sprite):
    
    # static class variables
    # image setup

    images = []
    images.append(create_circle_image(8, (255, 255, 0)))
    images.append(create_circle_image(8, (0, 255, 255)))

    hives = []
    hives.append((10, 20))
    hives.append((770, 570))

    angels = []
    angels.append(math.pi/4)
    angels.append(-math.pi/4)

    spread_length = 20.0
    speed = 70.0
    food_vision = 100
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

    def update(self, seconds):

        move_length = seconds * self.speed
        is_attracted = False

        closest_pheromone =  closest_object(self, Pheromone.groups[0])
        if (not (closest_pheromone is None)) and dist(closest_pheromone, self) < Ant.pheromone_vision:
            object_turn_to(self, closest_pheromone)
            is_attracted = True
        else:
            closest_enemy = closest_object(self, self.enemy_groups[0])
            if (not (closest_enemy is None)) and dist(closest_enemy, self) < Ant.enemy_vision:
                object_turn_to(self, closest_enemy)
                is_attracted = True
            else:
                closest_food =  closest_object(self, Food.groups[0])
                if (not (closest_food is None)) and dist(closest_food, self) < Ant.food_vision:
                    object_turn_to(self, closest_food)
                    is_attracted = True
    
        if not is_attracted:
            self.spread_length -= move_length
            if self.spread_length < 0:
                self.angle += random.uniform(-math.pi / 2.0, math.pi / 2.0)
                self.spread_length = Ant.spread_length
        else:
            self.spread_length = Ant.spread_length

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