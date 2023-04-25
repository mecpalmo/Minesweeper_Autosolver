import pyautogui
import cv2 as cv
import numpy as np

def getScreenshot():
    screenshot = pyautogui.screenshot()
    img = cv.cvtColor(np.array(screenshot), cv.COLOR_RGB2BGR)
    return img


def getFieldCenter(column, row, grid_details):
    x0, y0, square_side_length = grid_details
    x = x0 + column*square_side_length + 0.5*square_side_length
    y = y0 + row*square_side_length + 0.5*square_side_length
    return x, y


def clickLeft(_x, _y):
    pyautogui.click(_x, _y)

def clickRight(_x, _y):
    pyautogui.click(x= _x, y=_y, button='right')