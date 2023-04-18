import pyautogui
import numpy as np

import cv2 as cv

ss = pyautogui.screenshot()
ss = cv.cvtColor(np.array(ss), cv.COLOR_RGB2BGR)
cv.imshow('greyscale image',ss)
cv.waitKey(0)

