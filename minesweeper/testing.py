import cv2 as cv
import image_processing as ip
import screen_manager as sm
import random
from field_enum import Field_Content

TESTING = False

def performRandomSolving():

    grid_content, x0, y0, columns, rows, square_side_length = ip.getDefinedGrid(sm.getScreenshot())
    
    while(Field_Content.CLOSED_UNKNOWN.value in grid_content):
        screenshot = sm.getScreenshot() 
        grid_content, x0, y0, columns, rows, square_side_length = ip.getDefinedGrid(screenshot)
        grid_details = [x0, y0, square_side_length]
        if Field_Content.OPEN_MINE.value in grid_content:
            x, y = ip.getEmojiCenterPoint(screenshot)
            sm.clickLeft(x, y)
        random_column = random.randint(0, columns-1)
        random_row = random.randint(0, rows-1)
        if(grid_content[random_column, random_row] == Field_Content.CLOSED_UNKNOWN.value):
            x, y = sm.getFieldCenter(random_column, random_row, grid_details)
            sm.clickLeft(x, y)


def performTestRecognition():
    grid_content, x0, y0, columns, rows, square_side_length = ip.getDefinedGrid(getTestImage(6))


def getTestImage(index):
    image = cv.imread(f'./ss{index}.png',-1)
    image = cv.cvtColor(image, cv.COLOR_BGRA2BGR)
    return image


if(TESTING):
    print("test 1")
    _, _, columns, rows, _ = ip.getGridDetails(getTestImage(1))
    print(f"Grid: {columns}x{rows}, Should be: 30x16")

    print("test 2")
    _, _, columns, rows, _ = ip.getGridDetails(getTestImage(2))
    print(f"Grid: {columns}x{rows}, Should be: 30x16")

    print("test 3")
    _, _, columns, rows, _ = ip.getGridDetails(getTestImage(3))
    print(f"Grid: {columns}x{rows}, Should be: 9x9")

    print("test 4")
    _, _, columns, rows, _ = ip.getGridDetails(getTestImage(4))
    print(f"Grid: {columns}x{rows}, Should be: 9x9")

    print("test 5")
    _, _, columns, rows, _ = ip.getGridDetails(getTestImage(5))
    print(f"Grid: {columns}x{rows}, Should be: 30x16")



performTestRecognition()