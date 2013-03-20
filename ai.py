import math, random, setting
random.seed()

# gameData = [[player ant postion], [computer ant postion], [food],
#             [wall], [pheromone], [player hive], [computer hive]]

def dist(i, j):
    return math.hypot(i[0]-j[0], i[1]-j[1])

def closestObj(ant, objLst):
    closest = []
    if(len(objLst) > 0):
        closest = objLst[0]
    for obj in objLst:
        if(dist(ant, closest) > dist(ant, obj)):
            closest = obj
    return closest

def move(i, j, wall):
    u = random.randint(0, 1) # To random to move left/right, top/down.
    
    if (u == 0):
        if(i[0] > j[0] and wall.count([i[0] - 1, i[1]]) == 0):
            i[0] -= 1
        elif(i[0] < j[0] and wall.count([i[0] + 1, i[1]]) == 0):
            i[0] += 1
    if (u == 1):
        if(i[1] > j[1] and wall.count([i[0], i[1] + 1]) == 0):
             i[1] -= 1
        elif(i[1] < j[1] and wall.count([i[0], i[1] + 1]) == 0):
            i[1] += 1
    return i

def spread(ant, antLst):
    temp = ant
##    ally = closestObj(ant, antLst)
##
##    leftDis = ant[0] - ally[0]
##    topDis = ant[0] = ally[0]
##    dis = dist(ant, ally)
##
    i = random.random()

##    if(dis == 0):
    if(i < 0.5):
        temp[0] = temp[0] + 1
    else:
        temp[0] = temp[0] - 1
    i = random.random()
    if(i < 0.5):
        temp[1] = temp[1] + 1
    else:
        temp[1] = temp[1] - 1
##    else:
##        if(i < leftDis / dis):
##            temp[0] = temp[0] - 1
##        else:
##            temp[0] = temp[0] + 1
##        i = random.random()
##        if(i < toptDis / dis):
##            temp[1] = temp[1] - 1
##        else:
##            temp[1] = temp[1] + 1
    
    return temp 

##def spread(ant, antLst):
##    temp = []
##    lstSize = len(antLst)
##    # Find out how many ant on the left, top.
##    leftNum = 0
##    topNum = 0
##    for ally in antLst:
##        if (ant[0] > ally[0]):
##            leftNum += 1
##        if (ant[1] >  ally[1]):
##            topNum += 1
##            
##    i = random.random()
##    chance = (0.8 * float(leftNum)/float(lstSize)) + 0.10
##    if (i > chance):
##        temp.append(ant[0] - 1)
##    else:
##        temp.append(ant[0] + 1)
##
##    j = random.random()
##    chance = (0.8 * float(topNum)/float(lstSize)) + 0.10
##    if (j > chance):
##        temp.append(ant[1] - 1)
##    else:
##        temp.append(ant[1] + 1)
##    return temp 

def playerMove(gameData):
    for i, ant in enumerate(gameData[0]):
        # Check for closest nearby enemy ants.
        enemy = closestObj(ant, gameData[1])
        # Check if exist and within vision range
        if(not not enemy and dist(ant, enemy) <= setting.VISION):
            # Move toward it
            gameData[0][i] = move(ant, enemy, gameData[3])
            continue
        
        # Check the nearest food.
        food = closestObj(ant, gameData[2])
        # Check if within vision range
        if(not not food and dist(ant, food) <= setting.VISION):
            # Move toward it
            gameData[0][i] = move(ant, food, gameData[3])
            continue

        # Check the nearest pheromone.
        pheromone = closestObj(ant, gameData[4])
        # Check if within vision range
        if(not not pheromone and dist(ant, pheromone) <= setting.VISION):
            # Move toward it
            gameData[0][i] = move(ant, pheromone, gameData[3])
            continue

        # Spreadout around the hive.
        temp = spread(ant, gameData[0])
        gameData[0][i] = move(ant, temp, gameData[3])
