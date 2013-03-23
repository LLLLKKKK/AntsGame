import setting, random, pygame
from pygame.locals import *

random.seed()

def GetCenterPos(pos):
    return [pos[0]*8+4, pos[1]*8+4]

class Ants:
    def __init__(self, playerHive):
        self.hive = playerHive
        self.spawnRate = setting.ANT_SPAWN_RATE
        self.spawnCounter = 0
        
        self.ants = []
        self.index = 0

    def __iter__(self):
        return self

    def __len__(self):
        return len(self.ants)

    def __getitem__(self, index):
        return self.ants[index]
    
    def __setitem__(self, key, value):
        self.ants[key] = value

    def next(self):
        if self.index >= len(self.ants) - 1:
            raise StopIteration
        self.index = self.index + 1
        return self.ants[self.index]

    # Add spawned ant to the list of ants.
    def spawn(self):
        temp = [self.hive[0],self.hive[1]]
        self.spawnCounter += self.spawnRate
        for i in range(int(self.spawnCounter)):
            self.ants.append(temp)

    def eatFood(self):
        self.spawnRate += setting.FOOD_INCREASE_SPAWN_RATE

    def draw(self, screen, color):
        for ant in self.ants:
            pygame.draw.circle(screen, color, GetCenterPos(ant), 8)

class Foods:
    def __init__(self):
        self.spawnCounter = 0
        self.spawnRate = setting.FOOD_SPAWN_RATE

        self.foods = []
        self.index = 0

    def __iter__(self):
        return self

    def __len__(self):
        return len(self.foods)
        
    def __getitem__(self, index):
        return self.foods[index]

    def __setitem__(self, key, value):
        self.foods[key] = value

    def next(self):
        if self.index >= len(self.foods) - 1:
            raise StopIteration
        self.index = self.index + 1
        return self.foods[self.index]

    def spawn(self):
        if(len(self.foods) < setting.MAX_FOOD):
            self.spawnCounter += self.spawnRate
            for i in range(int(self.spawnCounter)):
                x = random.randint(0, setting.SIZE[0])
                y = random.randint(0, setting.SIZE[0])
                self.foods.append([x, y])


    
class Pheromones:
    def __init__(self):
        self.pheromones = []
        self.pheromonesTime = []
        self.index = 0

    def __iter__(self):
        return self

    def __len__(self):
        return len(self.pheromones)

    def __setitem__(self, key, value):
        self.pheromones[key] = value

    def next(self):
        if self.index >= len(self.pheromones) - 1:
            raise StopIteration
        self.index = self.index + 1
        return self.pheromones[self.index]

    def __getitem__(self, index):
        return self.pheromones[index]
    
    def spawn(self, pos):
        if(len(pheromones) > setting.MAX_PHEROMONE):
            pheromones.pop(0)
        pheromones.append(pos)
        pheromonesTime.append(setting.PHEROMONE_LIFETIME)

    def refresh(self):
        for i, x in enumerate(self.pheromonesTime):
            self.pheromonesTime[i] -= 1
            # remove pheromone with 0 lifetime
            if(self.pheromonesTime[i] <= 0):
                self.pheromones.remove(i)
                self.pheromonesTime.remove(i)
