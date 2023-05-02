import image_processing as ip
import screen_manager as sm
from field import Field
from field_enum import Field_Content
import random

def performOptimalSolving():

    grid_content, x0, y0, columns, rows, square_side_length = ip.getDefinedGrid(sm.getScreenshot())

    while(Field_Content.CLOSED_UNKNOWN.value in grid_content):
        
        screenshot = sm.getScreenshot()
        grid_content, x0, y0, columns, rows, square_side_length = ip.getDefinedGrid(screenshot)
        grid_details = [x0, y0, square_side_length]

        #print(grid_content)

        #collecting fields defining possible mine positions
        working_fields = []
        for i in range(0,columns):
            for j in range(0,rows):
                value = grid_content[i,j]
                if value in range(1,9):
                    working_fields.append(Field(generateID(i,j,rows), i, j, value))

        #generating solutions
        for field in working_fields:
            field.flags = countFlags(field.x, field.y, grid_content, columns, rows)
            field.bombs = int(field.value - field.flags)
            unknown_fields_ids = getUnknownFields(field.x, field.y, grid_content, columns, rows)
            field.generateSolutions(unknown_fields_ids)

        #comparing and eliminating solutions couple of times
        for i in range(0,2):
            for field_a in working_fields:
                for field_b in working_fields:
                    if len(field_a.solutions) > 0 and len(field_b.solutions) > 0 and field_a != field_b:
                        if len(set(field_a.solutions[0].keys()).intersection(set(field_b.solutions[0].keys()))) > 0:
                            newSolutions = []
                            for dict_a in field_a.solutions:
                                for dict_b in field_b.solutions:
                                    if are_dicts_overlapping(dict_a, dict_b):
                                        if dict_a not in newSolutions:
                                            newSolutions.append(dict_a)
                            field_a.solutions = newSolutions        
    
        #collecting executable solutions
        executable_solutions = {}
        for field in working_fields:
            if len(field.solutions) == 1:
                executable_solutions.update(field.solutions[0])
            sure_partial_solution = getSurePartialSolution(field.solutions)
            if len(sure_partial_solution) > 1:
                executable_solutions.update(sure_partial_solution)
            
        #executing found solutions
        print(f'Fields content determined: {executable_solutions}')
        executeSolution(executable_solutions, rows, grid_details)

        if len(executable_solutions) == 0:
            print("performing random shot")
            random_column = random.randint(0, columns-1)
            random_row = random.randint(0, rows-1)
            if(grid_content[random_column, random_row] == Field_Content.CLOSED_UNKNOWN.value):
                x, y = sm.getFieldCenter(random_column, random_row, grid_details)
                sm.clickLeft(x, y)

        if Field_Content.OPEN_MINE.value in grid_content:
            x, y = ip.getEmojiCenterPoint(screenshot)
            sm.clickLeft(x, y)
    
def getSurePartialSolution(solutions):
    sure_solution_dict = {}
    if len(solutions) > 0:
        for key in solutions[0].keys():
            value = solutions[0][key]
            if all(d[key] == value for d in solutions):
                sure_solution_dict[key] = value
    return sure_solution_dict


def executeSolution(solution, rows, grid_details):
    for id, value in solution.items():
        column, row = getCoordinatesFromID(id, rows)
        x, y = sm.getFieldCenter(column, row, grid_details)
        if value == 0:
            sm.clickLeft(x, y)
        if value == 1:
            sm.clickRight(x, y)


def are_dicts_overlapping(dict_a, dict_b):
    shared_keys = set(dict_a.keys()).intersection(set(dict_b.keys()))
    for key in shared_keys:
        if dict_a[key] != dict_b[key]:
            return False
    return True
            

def getUnknownFields(x, y, grid, cols, rows):
    unknown_fields_ids = []
    start_x = max(0, x-1)
    start_y = max(0, y-1)
    end_x = min(cols, x+2)
    end_y = min(rows, y+2)
    for i in range(start_x, end_x):
        for j in range(start_y, end_y):
            if grid[i,j] == Field_Content.CLOSED_UNKNOWN.value:
                unknown_fields_ids.append(generateID(i,j,rows))
    return unknown_fields_ids


def countFlags(x, y, grid, cols, rows):
    flags = 0
    start_x = max(0, x-1)
    start_y = max(0, y-1)
    end_x = min(cols, x+2)
    end_y = min(rows, y+2)
    for line in grid[start_x:end_x, start_y:end_y]:
        for item in line:
            if item == Field_Content.CLOSED_FLAG.value: flags+=1
    return flags


def generateID(x, y, rows):
    return x*rows + y


def getCoordinatesFromID(id, rows):
    return int(id/rows), (id % rows)