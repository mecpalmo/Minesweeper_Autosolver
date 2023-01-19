import image_processing as ir
import screen_manager as sm
import test
import random
import time

grid_content, x0, y0, columns, rows, square_side_length = ir.getDefinedGrid(sm.getScreenshot())

while(ir.CLOSED_UNKNOWN in grid_content):

    if ir.OPEN_MINE in grid_content:
        sm.click(ir.getEmojiCenterPoint)

    grid_content, x0, y0, columns, rows, square_side_length = ir.getDefinedGrid(sm.getScreenshot())
    grid_details = (x0, y0, square_side_length)

    random_column = random.randint(0, columns)
    random_row = random.randint(0, rows)

    if(grid_content[random_column, random_row] == ir.CLOSED_UNKNOWN):
        sm.click(sm.getFieldCenter(random_column, random_row, grid_details))

    time.sleep(0.5)



