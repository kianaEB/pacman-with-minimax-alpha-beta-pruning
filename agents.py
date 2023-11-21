from random import randint
from tree import DecisionTree
from tree import Node


class Pacman:
    def __init__(self, position = tuple(), inky_pos = tuple(), blinky_pos = tuple, food_positions = list(), wall_positions = list(), maxDepth = int): 
        self.position = position
        self.inky = inky_pos
        self.blinky = blinky_pos
        self.food = food_positions
        self.wall = wall_positions
        root = Node(self.position, self.inky, self.blinky, self.food, 0, self.wall, 0, 0)
        self.decision_tree = DecisionTree(root, maxDepth)
        self.next_moves = self.decision_tree.find_path()
        self.score = 0
        self.count_of_eaten_foods = 0
        self.count_of_moves = 0
        self.past_positions = None
        
    def update_decision_tree(self, maxDepth):
        root = Node(self.position, self.inky, self.blinky, self.food, 0, self.wall, 0, 0)
        self.decision_tree = None
        temp = DecisionTree(root, maxDepth)
        self.decision_tree = temp
        temp = None

    def update_next_moves(self, maxDepth):
        self.update_decision_tree(maxDepth)
        self.next_moves = self.decision_tree.find_path()
    
    def update_position(self):
        self.past_pos = self.position
        self.position = self.next_moves[0]
        self.next_moves.pop(0)
    
    def update_inky_pos(self, pos): 
        self.inky = pos
    
    def update_blinky_pos(self, pos): 
        self.blinky = pos
    
    def update_food_pos(self):
        if self.position in self.food:
            self.food.remove(self.position)
            self.count_of_eaten_foods += 1

    def update_count_of_move(self):
        if self.past_positions != self.position:
            self.count_of_moves += 1
    
    def update_score(self):
        return (10 * self.count_of_eaten_foods - self.count_of_moves)

    position = tuple()
    inky = tuple()
    blinky = tuple()
    wall = list()
    food = list()
    next_moves = list()
    count_of_eaten_foods = int()
    score = int()

class Ghost:
    def __init__(self, position = tuple(), pacmanPos = tuple(), friendPos = tuple(), wallPoses = list()):
        self.position = position
        self.pacman_pos = pacmanPos
        self.friend_pos = friendPos
        self.wall_poses = wallPoses

    def get_next_move(self):
        direction = randint(1, 4)
        if direction == 1: self.next_move = (1, 0)
        if direction == 2: self.next_move = (0, 1)
        if direction == 3: self.next_move = (-1, 0)
        if direction == 4: self.next_move = (0, -1)
        return self.next_move
    
    def update_position(self):
        self.next_move = self.get_next_move()
        temp = self.__addToPosition(self.position, self.next_move)
        if temp not in self.wall_poses and temp not in self.friend_pos:
            self.position = temp
    
    def update_pacman_pos(self, pos): 
        self.pacman_pos = pos

    def update_friend_pos(self, pos):
        self.friend_pos = pos

    def __addToPosition(self, a, b):  
        return (a[0] + b[0], a[1] + b[1])

    position = tuple()
    pacman_pos = tuple()
    friend_pos = tuple()
    wall_poses = list(tuple())
    next_move = tuple()