import cv2 as cv
import pyautogui
import numpy as np
from collections import Counter

def getScreenImage():
    screenshot = pyautogui.screenshot()
    img = cv.cvtColor(np.array(screenshot), cv.COLOR_RGB2BGR)
    return img

def getGridLocationList(screenshot):

    #convert image to hvs to filter out based on vibration
    hsv = cv.cvtColor(screenshot, cv.COLOR_BGR2HSV)
    
    #filter out only certain shades of gray areas
    lower_thres = np.array([0, 0, 130])
    upper_thres = np.array([0, 0, 200])
    game_mask = cv.inRange(hsv, lower_thres, upper_thres)

    #delete little particles
    kernel = np.ones((3, 3), np.uint8)
    game_mask = cv.erode(game_mask, kernel)
    
    #find all contours on mask showing only game areas
    game_contours, _ = cv.findContours(game_mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    rec_contours = []
    areas = []
    #filter out only contours shaped similar to a rectangle
    for cnt in game_contours:
        approx = cv.approxPolyDP(cnt, 0.01*cv.arcLength(cnt, True), True)
        if len(approx) == 4:
            area = cv.contourArea(cnt)
            areas.append(area)
            rec_contours.append(cnt)
    
    #sort rectangle contours by size from highest to lowest
    rec_contours = sorted(rec_contours, key=cv.contourArea, reverse=True)
    
    #create a mask containing only the grid area of the game (assuming it's 2nd biggest contour)
    field_mask = np.zeros((game_mask.shape),np.uint8)
    cv.drawContours(field_mask, [rec_contours[1]], -1, color=(255, 255, 255), thickness=cv.FILLED)
    
    #make the rectangle a bit smaller and smoother as the contour was a bit too big
    kernel = np.ones((5, 5), np.uint8)
    field_mask = cv.erode(field_mask, kernel)
    field_mask = cv.erode(field_mask, kernel)
    #field_mask = cv.erode(field_mask, kernel)
    cv.imshow("field_mask",field_mask)
    cv.waitKey(0)
    
    #use field_mask to filter out the grid from og image
    og_gray = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
    grid_img = cv.bitwise_and(og_gray, og_gray, mask=field_mask)
    cv.imshow("grid",grid_img)
    cv.waitKey(0)
    
    #enhance the histogram or sth to enhance edges, maybe dilate, erode
    grid_img = cv.equalizeHist(grid_img)
    #grid_img = cv.erode(grid_img, kernel)
    cv.imshow("grid",grid_img)
    cv.waitKey(0)
    
    edges = cv.Canny(grid_img,100,300,apertureSize = 3)
    edges = cv.dilate(edges, kernel = np.ones((2, 2), np.uint8))
    edges = cv.dilate(edges, kernel = np.ones((2, 2), np.uint8))
    edges = cv.erode(edges, kernel= np.ones((2,2), np.uint8))
    edges = cv.erode(edges, kernel= np.ones((2,2), np.uint8))
    #edges = cv.dilate(edges, kernel = np.ones((2, 2), np.uint8))
    cv.imshow("Canny",edges)
    cv.waitKey(0)

    #find all contours in that image
    grid_contours, _ = cv.findContours(edges, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    #cv.drawContours(screenshot, grid_contours, -1, (0, 255, 0), 1)
    #filter out only rectangles
    rec_contours = []
    #create a list of rectangles positions
    field_coordinates = []
    #filter out only contours shaped similar to a rectangle
    for cnt in grid_contours:
        approx = cv.approxPolyDP(cnt, 0.05*cv.arcLength(cnt, True), True)
        if len(approx) == 4:
            area = cv.contourArea(cnt)
            areas.append(area)
            rec_contours.append(cnt)
            n = approx.ravel() 
            x1 = n[0] 
            y1 = n[1]
            x2 = n[4]
            y2 = n[5]
            ratio = abs((x1-x2)/(y1-y2))
            if(ratio < 1.2 and ratio > 0.8):
                field_coordinates.append([x1,y1])

    #painting points to check
    for f in field_coordinates:
        screenshot = cv.circle(screenshot, (f[0],f[1]), radius=2, color=(0, 0, 255), thickness=-1)
        #screenshot = cv.circle(screenshot, (f[2],f[3]), radius=2, color=(255, 0, 0), thickness=-1)

    cv.imshow("points",screenshot)
    cv.waitKey(0)

    #getting positions of fields
    field_coordinates = np.array(field_coordinates)
    xs = field_coordinates[:, 0]
    ys = field_coordinates[:, 1]

    x_dict = dict(Counter(xs))
    y_dict = dict(Counter(ys))

    x_dict_2 = { }
    y_dict_2 = { }

    for key in x_dict.keys():
        if(x_dict[key]!=1):
            x_dict_2[key] = x_dict[key]

    for key in y_dict.keys():
        if(y_dict[key]!=1):
            y_dict_2[key] = y_dict[key]

    xs = x_dict_2.keys()
    ys = y_dict_2.keys()

    xs = sorted(xs)
    ys = sorted(ys)

    #getting most common field width
    x_spaces = []
    y_spaces = []
    
    for i in range(0, len(xs)-1):
        x_spaces.append(xs[i+1]-xs[i])

    for i in range(0, len(ys)-1):
        y_spaces.append(ys[i+1]-ys[i])

    x_space = np.max(x_spaces)
    y_space = np.max(y_spaces)

    print(f"x_space: {x_space}")
    print(f"y_space: {y_space}")

    #getting the width and height of the entire grid
    field_mask_contour, _ = cv.findContours(field_mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    sorted(field_mask_contour, reverse=True)
    x0, y0, width, height = cv.boundingRect(field_mask_contour[0])

    #get grid size
    columns = int((width)/(x_space))
    rows = int((height)/(x_space))

    print(f"Width: {width}, Height: {height}")
    print(f"Columns: {columns}, Rows: {rows}")

    grid = []
    
    for i in range(0, rows):
        row = []
        for j in range(0, columns):
            x = x0 + j*x_space
            y = y0 + i*x_space
            row.append([x, y])
        grid.append(row)

    return grid


def getEmojiCenter(screenshot):

    hsv = cv.cvtColor(screenshot, cv.COLOR_BGR2HSV)
    lower_thres = np.array([0, 0, 130])
    upper_thres = np.array([0, 0, 200])
    game_mask = cv.inRange(hsv, lower_thres, upper_thres)
    kernel = np.ones((3, 3), np.uint8)
    game_mask = cv.erode(game_mask, kernel) 
    game_contours, _ = cv.findContours(game_mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    rec_contours = []
    areas = []
    for cnt in game_contours:
        approx = cv.approxPolyDP(cnt, 0.02*cv.arcLength(cnt, True), True)
        if len(approx) == 4:
            area = cv.contourArea(cnt)
            areas.append(area)
            rec_contours.append(cnt)
    rec_contours = sorted(rec_contours, key=cv.contourArea, reverse=True)
    gray_screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
    bar_mask = np.zeros((gray_screenshot.shape),np.uint8)
    cv.drawContours(bar_mask, [rec_contours[2]], -1, color=(255, 255, 255), thickness=cv.FILLED)
    lower_thres = np.array([10, 20, 50])
    upper_thres = np.array([70, 255, 255])
    yellow_mask = cv.inRange(hsv, lower_thres, upper_thres)
    yellow_mask = cv.dilate(yellow_mask, kernel) 
    emoji_mask = cv.bitwise_and(yellow_mask, yellow_mask, mask=bar_mask)
    emoji_contours, _ = cv.findContours(emoji_mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    emoji_contours = sorted(emoji_contours, key=cv.contourArea, reverse=True)
    M = cv.moments(emoji_contours[0])
    x = int(M["m10"] / M["m00"])
    y = int(M["m01"] / M["m00"])
    
    pyautogui.click(x, y)