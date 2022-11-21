import cv2 as cv
import pyautogui
import numpy as np

ss = cv.imread('ss2.png',-1)
ss = cv.cvtColor(ss, cv.COLOR_BGRA2BGR)

def getScreenImage():
    
    screenshot = pyautogui.screenshot()
    img = cv.cvtColor(np.array(screenshot), cv.COLOR_RGB2BGR)
    #cv.imshow("screenshot", img)
    #cv.waitKey(0)
    return img

#ss = getScreenImage()

def getFieldContour(screenshot):
    hsv = cv.cvtColor(screenshot, cv.COLOR_BGR2HSV)
    lower_thres = np.array([0, 0, 130])
    upper_thres = np.array([0, 0, 200])
    game_mask = cv.inRange(hsv, lower_thres, upper_thres)
    kernel = np.ones((3, 3), np.uint8)
    game_mask = cv.erode(game_mask, kernel)
    #game_mask = cv.dilate(game_mask, kernel)
    cv.imshow("game_mask", game_mask)
    cv.waitKey(0)
    game_contours, _ = cv.findContours(game_mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    rec_contours = []
    areas = []
    for cnt in game_contours:
        cv.drawContours(ss, [cnt], -1, (255,0,0), 1)
        approx = cv.approxPolyDP(cnt, 0.01*cv.arcLength(cnt, True), True)
        if len(approx) == 4:
            cv.drawContours(ss, [cnt], -1, (0,0,255), 1)
            area = cv.contourArea(cnt)
            areas.append(area)
            rec_contours.append(cnt)
    
    rec_contours = sorted(rec_contours, key=cv.contourArea, reverse=True)
    
    x, y, field_width, field_height = cv.boundingRect(rec_contours[1])
    x = x+2
    y = y+2
    field_width = field_width - 4
    field_height = field_height - 4

    field_mask = np.zeros((game_mask.shape),np.uint8)
    cv.drawContours(field_mask, [rec_contours[1]], -1, color=(255, 255, 255), thickness=cv.FILLED)
    
    cv.imshow("grid_mask", grid_mask)
    cv.waitKey(0)


def clickEmojiCenter(screenshot):

    hsv = cv.cvtColor(screenshot, cv.COLOR_BGR2HSV)
    lower_thres = np.array([0, 0, 130])
    upper_thres = np.array([0, 0, 200])
    game_mask = cv.inRange(hsv, lower_thres, upper_thres)
    kernel = np.ones((3, 3), np.uint8)
    game_mask = cv.erode(game_mask, kernel) 
    #cv.imshow("game_mask", game_mask)
    #cv.waitKey(0)
    game_contours, _ = cv.findContours(game_mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    rec_contours = []
    areas = []
    for cnt in game_contours:
        #cv.drawContours(ss, [cnt], -1, (255,0,0), 1)
        approx = cv.approxPolyDP(cnt, 0.02*cv.arcLength(cnt, True), True)
        if len(approx) == 4:
            #cv.drawContours(ss, [cnt], -1, (0,0,255), 1)
            area = cv.contourArea(cnt)
            areas.append(area)
            rec_contours.append(cnt)
    rec_contours = sorted(rec_contours, key=cv.contourArea, reverse=True)
    cv.drawContours(ss, [rec_contours[2]], -1, (0,0,255), 1)
    gray_screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
    bar_mask = np.zeros((gray_screenshot.shape),np.uint8)
    cv.drawContours(bar_mask, [rec_contours[2]], -1, color=(255, 255, 255), thickness=cv.FILLED)
    lower_thres = np.array([10, 20, 50])
    upper_thres = np.array([70, 255, 255])
    yellow_mask = cv.inRange(hsv, lower_thres, upper_thres)
    yellow_mask = cv.dilate(yellow_mask, kernel) 
    #cv.imshow("yellow_mask", yellow_mask)
    #cv.waitKey(0)
    emoji_mask = cv.bitwise_and(yellow_mask, yellow_mask, mask=bar_mask)
    #cv.imshow("emoji_mask", emoji_mask)
    #cv.waitKey(0)
    emoji_contours, _ = cv.findContours(emoji_mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    emoji_contours = sorted(emoji_contours, key=cv.contourArea, reverse=True)
    cv.drawContours(ss, [emoji_contours[0]], -1, (0,255,0), 1)
    M = cv.moments(emoji_contours[0])
    x = int(M["m10"] / M["m00"])
    y = int(M["m01"] / M["m00"])
    pyautogui.click(x, y)
    

#ss = cv.drawContours(ss, [getFieldContour(ss)], -1, (0,255,0), 2)
#clickEmojiCenter(ss)
getFieldContour(ss)

cv.imshow("field_contour", ss)
cv.waitKey(0)