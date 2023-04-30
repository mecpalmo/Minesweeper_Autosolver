import itertools

class Field:

    def __init__(self, _id, _x, _y, _value):
        self.id = _id
        self.x = _x
        self.y = _y
        self.value = _value

        self.flags = 0
        self.bombs = 0
        self.solutions = []
    
    def generateSolutions(self, unknown_fields_ids):
        n = len(unknown_fields_ids)
        k = self.bombs
        self.solutions = []
        if self.bombs == 0:
            solution = {}
            for id in unknown_fields_ids:
                solution.update({id: 0})
            self.solutions.append(solution)
        if self.bombs > 0:
            for indices in itertools.combinations(range(n), k):
                arr = [0] * n
                for i in indices:
                    arr[i] = 1
                self.solutions.append( {id: content for id, content in zip(unknown_fields_ids, arr)} )