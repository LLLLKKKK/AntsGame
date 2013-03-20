import setting, random

random.seed()

class SpawnAnt:
    def __init__(self, playerHive):
        self.hive = playerHive
        self.spawnRate = setting.ANT_SPAWN_RATE
        self.spawnCounter = 0

    # Add spawned ant to the list of ants.
    def spawn(self, ant):
        temp = [self.hive[0],self.hive[1]]
        self.spawnCounter += self.spawnRate
        for i in range(int(self.spawnCounter)):
            ant.append(temp)

    def eatFood(self):
        self.spawnRate += setting.FOOD_INCREASE_SPAWN_RATE

    

class SpawnFood:
    def __init__(self):
        self.spawnCounter = 0
        self.spawnRate = setting.FOOD_SPAWN_RATE

    def spawn(self, food):
        self.spawnCounter += self.spawnRate
        for i in range(int(self.spawnCounter)):
            x = random.randint(0, setting.SIZE[0])
            y = random.randint(0, setting.SIZE[0])
            food.append([x, y])
        
        

