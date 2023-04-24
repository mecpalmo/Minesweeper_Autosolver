import image_processing as ip
import screen_manager as sm
from logic_classes.Field import Field
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

    for field_a in working_fields:
        for field_b in working_fields:
            if field_a != field_b:
                if set(field_b.unknown_fields_ids).issubset(set(field_a.unknown_fields_ids)):
                    field_a_dicts = []
                    field_b_dicts = []
                    for solution in field_a.solutions:
                        field_a_dicts.append( {id: content for id, content in zip(field_a.unknown_fields_ids, solution)} )
                    for solution in field_b.solutions:
                        field_b_dicts.append( {id: content for id, content in zip(field_b.unknown_fields_ids, solution)} )
                    
                    

                    
    # dla każdego pracującego pola znajdź inne pola które mają tabelę otaczających pól całkowicie zawierającą się
    # w obecnie rozpatrywanym polu

    # po znalezieniu takiej pary wyeliminuj rozwiązania z tabeli rozwiązań, które się nie pokrywają

    # może się okazać, że wczyszczenie jakiejś tabeli wpłynęłoby na czyszczenie tabeli pola, które było rozpatrywane
    # wcześniej, przez co dopiero w kolejnej iteracji zostanie to osiągnięte

    # po wykonaniu jednej serii czyszczenia, wybieramy pola które w tabeli rozwiązań mają tylko jedno rozwiązanie
    # jeżeli nie ma takiego ani jednego pola, ponawiamy czyszczenie 5 razy, jeśli wciąż nie ma takiego pola,
    # musimy kliknąć w losowe pole

    # ponawiamy całą funkcję od samego początku póki występują jakieś nieznane pola


def getUnknownFields(x, y, grid, cols, rows):

    fields = []
    start_x = max(0, x-1)
    start_y = max(0, y-1)
    end_x = min(cols, x+2)
    end_y = min(rows, y+2)
    for i in range(start_x, end_x):
        for j in range(start_y, end_y):
            if grid[i,j] == Field_Content.CLOSED_UNKNOWN.value:
                fields.append(generateID(i,j))
    return fields


def countFlags(x, y, grid, cols, rows):

    flags = 0
    start_x = max(0, x-1)
    start_y = max(0, y-1)
    end_x = min(cols, x+2)
    end_y = min(rows, y+2)
    for field in grid[start_x:end_x, start_y:end_y]:
        if field == Field_Content.CLOSED_FLAG.value: flags+=1
    return flags


def generateID(x, y, columns):

    return x*columns + y