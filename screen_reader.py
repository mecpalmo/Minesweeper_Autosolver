import cv2 as cv
import pyautogui
import numpy as np

ss = cv.imread('ss2.png',-1)
ss = cv.cvtColor(ss, cv.COLOR_BGRA2BGR)

def getScreenImage():
    
    screenshot = pyautogui.screenshot()
    return cv.cvtColor(np.array(screenshot), cv.COLOR_RGB2BGR)


def getFieldContour(screenshot):
    
    hsv = cv.cvtColor(screenshot, cv.COLOR_BGR2HSV)
    
    lower_thres = np.array([0, 0, 130])
    upper_thres = np.array([0, 0, 200])

    game_mask = cv.inRange(hsv, lower_thres, upper_thres)
    kernel = np.ones((3, 3), np.uint8)
    game_mask = cv.erode(game_mask, kernel) 

    cv.imshow("game_mask", game_mask)
    cv.waitKey(0)

    game_contours, _ = cv.findContours(game_mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    rec_contours = []
    areas = []

    for cnt in game_contours:
        cv.drawContours(ss, [cnt], -1, (255,0,0), 1)
        approx = cv.approxPolyDP(cnt, 0.02*cv.arcLength(cnt, True), True)
        if len(approx) == 4:
            cv.drawContours(ss, [cnt], -1, (0,0,255), 1)
            area = cv.contourArea(cnt)
            areas.append(area)
            rec_contours.append(cnt)

    rec_contours = sorted(rec_contours, key=cv.contourArea, reverse=True)

    return rec_contours[1] #podatne na błędy

ss = cv.drawContours(ss, [getFieldContour(ss)], -1, (0,255,0), 3)
cv.imshow("field_contour", ss)
cv.waitKey(0)