import cv2 as cv
import pyautogui
import numpy as np

def getScreenImage():
    screenshot = pyautogui.screenshot()
    return cv.cvtColor(np.array(screenshot), cv.COLOR_RGB2BGR)

def getFieldContour(screenshot):
    hsv = cv.cvtColor(screenshot, cv.COLOR_BGR2HSV)
    
    lower_thres = np.array([0, 0, 130])
    upper_thres = np.array([0, 0, 200])

    game_mask = cv.inRange(hsv, lower_thres, upper_thres)
    #kernel = np.ones((3, 3), np.uint8)
    #game_mask = cv.erode(game_mask, kernel) 

    cv.imshow("game_mask", game_mask)
    cv.waitKey(0)

    game_contours, _ = cv.findContours(game_mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    areas = []
    for i in game_contours:
        area = cv.contourArea(i)
        areas.append(area)

    game_Contours = sorted(game_contours, key=cv.contourArea, reverse=True)

ss = cv.imread('ss1.png',-1)
ss = cv.cvtColor(ss, cv.COLOR_BGRA2BGR)

getFieldContour(ss)