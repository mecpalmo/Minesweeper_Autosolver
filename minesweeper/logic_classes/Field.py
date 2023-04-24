import itertools
from Solution import Solution

class Field:

    def __init__(self, _id, _x, _y, _value):
        self.id = _id
        self.x = _x
        self.y = _y
        self.value = _value

        self.flags = 0
        self.bombs = 0
        self.unknown_fields_ids = []

    def __init__(self):
        ...
    
    def generateSolutions(self):
        n = len(self.unknown_fields_ids)
        k = self.bombs
        self.solutions = []
        for indices in itertools.combinations(range(n), k):
            arr = [0] * n
            for i in indices:
                arr[i] = 1
            self.solutions.append(arr)
            


field = Field()

field.unknown_fields_ids = [0, 1, 2, 3, 4]
field.bombs = 3

print("start") 

field.generateSolutions()