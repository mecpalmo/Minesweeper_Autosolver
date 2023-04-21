import math
#from Solution import Solution

class Field:

    def __init__(self, _id, _x, _y, _value):
        self.id = _id
        self.x = _x
        self.y = _y
        self.value = _value

        self.flags = 0
        self.bombs = 0
        self.unknown_fields_ids = []
    
    def generateSolutions(self):
        self.solutions = []
        combinations = math.comb(len(self.unknown_fields_ids), self.bombs)
        for i in range (0,combinations):
            ...