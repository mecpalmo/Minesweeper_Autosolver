import image_processing as ir
import screen_manager as sm
import test
import random
import time

grid_content, x0, y0, columns, rows, square_side_length = ir.getDefinedGrid(sm.getScreenshot())

while(ir.CLOSED_UNKNOWN in grid_content):

    screenshot = sm.getScreenshot() 

    grid_content, x0, y0, columns, rows, square_side_length = ir.getDefinedGrid(screenshot)
    grid_details = [x0, y0, square_side_length]
    
    if ir.OPEN_MINE in grid_content:
        x, y = ir.getEmojiCenterPoint(screenshot)
        sm.click(x, y)

    random_column = random.randint(0, columns-1)
    random_row = random.randint(0, rows-1)

    if(grid_content[random_column, random_row] == ir.CLOSED_UNKNOWN):
        x, y = sm.getFieldCenter(random_column, random_row, grid_details)
        sm.click(x, y)

    time.sleep(0.1)