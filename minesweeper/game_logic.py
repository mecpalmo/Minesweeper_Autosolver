import image_processing as ip
import screen_manager as sm
from field_enum import Field_Content

def performOptimalSolving():

    grid_content, x0, y0, columns, rows, square_side_length = ip.getDefinedGrid(sm.getScreenshot())

    working_fields = []

    for i in range(0,columns):
        for j in range(0,rows):
            value = grid_content[i, j]
            if value in range(1,9):
                id = generateID(i,j,columns)
                working_fields.append(Field(id, i, j, value))

    for field in working_fields:
        field.flags = countFlags(field.x, field.y, grid_content, columns, rows)
        field.bombs = field.value - field.flags
        field.unknown_fields_ids = getUnknownFields(field.x, field.y, grid_content, columns, rows)
        field.generateSolutions()

def getUnknownFields(x, y, grid, cols, rows):
    fields = []
    start_x = max(0, x-1)
    start_y = max(0, y-1)
    end_x = min(cols, x+2)
    end_y = min(rows, y+2)
    for i in range(start_x, end_x):
        for j in range(start_y, end_y):
            if grid[i,j] == Field_Content.CLOSED_UNKNOWN:
                fields.append(generateID(i,j))
    return fields

def countFlags(x, y, grid, cols, rows):
    flags = 0
    start_x = max(0, x-1)
    start_y = max(0, y-1)
    end_x = min(cols, x+2)
    end_y = min(rows, y+2)
    for field in grid[start_x:end_x, start_y:end_y]:
        if field == Field_Content.CLOSED_FLAG: flags+=1
    return flags

def generateID(x, y, columns):
    return x*columns + y

class Field:
    def __init__(self, _id, _x, _y, _value):
        self.id = _id
        self.x = _x
        self.y = _y
        self.value = _value
    
    def generateSolutions(self):
        self.solutions = []
        #trzeba obliczyć ile jest kombinacji. dwumian newtona: math.comb(n, k)
        #wybierz k elementów na n miejsc
        

class Solution:
    def __init__(self):
        self.field_guesses = []

    def generateSolution(self, _x, _y, _bomb):
        self.field_guesses.append(Field_guess(_x, _y, _bomb))

class Field_guess:
    def __init__(self, _id, _x, _y, _bomb):
        self.id = _id
        self.x = _x
        self.y = _y
        self.bomb = _bomb #True or False