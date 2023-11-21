import sys

class Node:
    def __init__(self, pacmanPos = tuple(), inkyPos = tuple(), blinkyPos = tuple(), dotPoses = list(), countOfDotsEaten = int(), wallPoses = list(), countOfMovesOfPacman = int(), depth = int()):
        self.pacman = pacmanPos
        self.inky = inkyPos
        self.blinky = blinkyPos
        self.food = dotPoses
        self.count_of_food_eaten = countOfDotsEaten
        self.wall = wallPoses
        self.count_of_moves_of_pacman = countOfMovesOfPacman
        self.depth = depth
        self.children = []
        self.father = None

        pacmanPos = tuple()
        inkyPos = tuple()
        blinkyPos = tuple()
        dotPoses = list()
        countOfDotsEaten = int()
        countOfMovesOfPacman = int()
        wallPoses = list()
        depth = int()
        #children = list()

class DecisionTree:
    def __init__(self, root = Node(), maxDepth = int()):
        self.root = root
        self.maxDepth = maxDepth
        self.leaves = []
        self.buildTree()
    
    def buildTree(self):
        queue = list()
        node = self.root
        queue.append(node)   

        while len(queue) != 0:
            node = queue.pop(0)
            
            direction = [(1, 0), (0, 1), (-1, 0), (0, -1)]

            if node.depth % 3 == 0:
                for i in range(0, 4):
                    child_pacman = self.__addToPositionForPacman(node.pacman, direction[i], node.wall)
                    child_inky = node.inky
                    child_blinky = node.blinky
                    if child_pacman in node.food:
                        child_food = node.food.copy()
                        child_food.remove(child_pacman)
                        child_count_of_food_eaten = node.count_of_food_eaten + 1
                    else:
                        child_food = node.food.copy()
                        child_count_of_food_eaten = node.count_of_food_eaten
                    child_wall= node.wall.copy()
                    
                    if child_pacman != node.pacman:
                        child_count_of_moves_of_pacman = node.count_of_moves_of_pacman + 1
                    else:
                        child_count_of_moves_of_pacman = node.count_of_moves_of_pacman
                    child_depth = node.depth + 1
                    child = Node(child_pacman, child_inky, child_blinky, child_food, child_count_of_food_eaten, child_wall, child_count_of_moves_of_pacman, child_depth)
                    child.father = node
                    node.children.append(child)
            
            elif node.depth % 3 == 1:
                for i in range(0, 4):
                    child_pacman = node.pacman
                    child_inky = self.__addToPositionForGhosts(node.inky, direction[i], child_blinky, node.wall)
                    child_blinky = node.blinky
                    child_food = node.food.copy()
                    child_count_of_food_eaten = node.count_of_food_eaten
                    child_wall = node.wall.copy()
                    child_count_of_moves_of_pacman = node.count_of_moves_of_pacman
                    child_depth = node.depth + 1
                    child = Node(child_pacman, child_inky, child_blinky, child_food, child_count_of_food_eaten, child_wall, child_count_of_moves_of_pacman, child_depth)
                    child.father = node
                    node.children.append(child)
            
            elif node.depth % 3 == 2:
                for i in range(0, 4):
                    child_pacman = node.pacman
                    child_inky = node.inky
                    child_blinky = self.__addToPositionForGhosts(node.blinky, direction[i], child_inky, node.wall)
                    child_food = node.food.copy()
                    child_count_of_food_eaten = node.count_of_food_eaten
                    child_wall = node.wall.copy()
                    child_count_of_moves_of_pacman = node.count_of_moves_of_pacman
                    child_depth = node.depth + 1
                    child = Node(child_pacman, child_inky, child_blinky, child_food, child_count_of_food_eaten, child_wall, child_count_of_moves_of_pacman, child_depth)
                    child.father = node
                    node.children.append(child)
            
            if node.children[3].depth != self.maxDepth:
                for i in range(0, 4):
                    queue.append(node.children[i])
            else:
                for i in range(0, 4):
                    self.leaves.append(node.children[i])
        self.eUtility()
    
    def eUtility(self):
        for leaf in self.leaves:
            g = 10 * leaf.count_of_food_eaten - leaf.count_of_moves_of_pacman
            distanceToClosestGhost = min(self.__manhattanDistance(leaf.pacman, leaf.inky), self.__manhattanDistance(leaf.pacman, leaf.blinky))
            countOfNearWalls = self.__countOfNearWalls(leaf)
            h = distanceToClosestGhost - countOfNearWalls
            f = g + h
            self.utilities[leaf] = f

    def _minimax(self, node, alpha, beta):
        if node.depth == self.maxDepth:
            return self.utilities[node], node
        
        if node.depth % 3 == 0:
            utility = -sys.maxsize
            for child in node.children:
                newUtility, newNode = self._minimax(child, alpha, beta)
                if newUtility > utility:
                    utility = newUtility
                    optimalNode = newNode
                alpha = max(alpha, utility)
                if beta <= alpha:
                    break
            return utility, optimalNode
        else:
            utility = sys.maxsize
            for child in node.children:
                newUtility, newNode = self._minimax(child, alpha, beta)
                if newUtility < utility:
                    utility = newUtility
                    optimalNode = newNode
                beta = min(beta, utility)
                if beta <= alpha:
                    break
            return utility, optimalNode

    def alphaBetaPruning(self):
        alpha = -sys.maxsize
        beta = sys.maxsize
        utility, optimalNode = self._minimax(self.root, alpha, beta)
        return utility, optimalNode

    def find_path(self):
        _, optimalNode = self.alphaBetaPruning()
        maximizingPlayerPoses = []
        node = optimalNode
        while node.father is not None:
            if node.depth % 3 == 0:
                maximizingPlayerPoses.append(node.pacman)
            node = node.father
        maximizingPlayerPoses.reverse()
        return maximizingPlayerPoses

    def __addToPositionForPacman(self, a, b, wall):
        if (a[0] + b[0], a[1] + b[1]) in wall:
            return a
        else:
            return (a[0] + b[0], a[1] + b[1])
    
    def __addToPositionForGhosts(self, a, b, friendPos, wallPoses):
        if (a[0] + b[0], a[1] + b[1]) in wallPoses or (a[0] + b[0], a[1] + b[1]) == friendPos:
            return a
        else:
            return (a[0] + b[0], a[1] + b[1])
        
    def __addToPosition(self, a, b):
        return  (a[0] + b[0], a[1] + b[1])

    def __manhattanDistance(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def __countOfNearWalls(self, node):
        count = 0
        nearDirections = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
        for i in range(0, 8):
            direction = nearDirections[i]
            if self.__addToPosition(node.pacman, direction) in node.wall:
                count += 1
        return count

    root = Node(tuple(), tuple(), tuple(), list(), list(), int())
    maxDepth = int()
    leaves = list()
    utilities = dict()