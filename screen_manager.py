import pyautogui
import cv2 as cv
import numpy as np


def getScreenshot():
    screenshot = pyautogui.screenshot()
    img = cv.cvtColor(np.array(screenshot), cv.COLOR_RGB2BGR)
    return img

def click(x, y):
    pyautogui.click(x, y)