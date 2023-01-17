import cv2 as cv
import pyautogui
import numpy as np
from collections import Counter



def getScreenshot():
    screenshot = pyautogui.screenshot()
    img = cv.cvtColor(np.array(screenshot), cv.COLOR_RGB2BGR)
    return img



def getGrid(screenshot):

    game_image = getGameImage(screenshot)
    game_image_gray = cv.cvtColor(game_image, cv.COLOR_BGR2GRAY)
    game_canny = cv.Canny(game_image_gray, 100, 300, apertureSize = 3)
    cv.imshow("game_canny", game_canny)
    cv.waitKey(0)
    game_contours, _ = cv.findContours(game_image_gray, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    rectangle_contours = filterRectangleContours(game_contours)
    rectangle_contours = sorted(rectangle_contours, key=cv.contourArea, reverse=True)
    drawContours(game_image_gray, rectangle_contours)
    #I'm assuming the 2nd biggest rectangle contour is around the grid
    grid_mask = np.zeros((game_image.shape[:2]), np.uint8)
    cv.drawContours(grid_mask, [rectangle_contours[1]], -1, color=(255, 255, 255), thickness=cv.FILLED)
    #the grid mask needs to be smoothened out. We need it quite precise
    cv.erode(grid_mask, kernel=np.ones((5, 5), np.uint8))
    cv.erode(grid_mask, kernel=np.ones((5, 5), np.uint8))
    cv.imshow("field_mask",grid_mask)
    cv.waitKey(0)
    
    grid_image = cv.bitwise_and(game_image, game_image, mask=grid_mask)
    #grid_image = cv.equalizeHist(grid_img)
    cv.imshow("grid",grid_image)
    cv.waitKey(0)
    
    edges = cv.Canny(grid_image,100,300,apertureSize = 3)
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
            rec_contours.append(cnt)
            n = approx.ravel() 
            x1 = n[0] 
            y1 = n[1]
            x2 = n[4]
            y2 = n[5]
            ratio = abs((x1-x2)/(y1-y2))
            if(ratio < 1.2 and ratio > 0.8):
                field_coordinates.append([x1,y1])

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
    field_mask_contour, _ = cv.findContours(grid_mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    sorted(field_mask_contour, reverse=True)
    x0, y0, width, height = cv.boundingRect(field_mask_contour[0])

    #get grid size
    columns = int((width)/(x_space))
    rows = int((height)/(x_space))

    print(f"Width: {width}, Height: {height}")
    print(f"Columns: {columns}, Rows: {rows}")

    grid = []
    
    for i in range(0, columns):
        column = []
        for j in range(0, rows):
            x = x0 + i*x_space
            y = y0 + j*x_space
            column.append([x, y])
        grid.append(column)

    grid = np.array(grid)

    return grid, x_space




def getFieldImage(screenshot, column, row):
    
    gridArray, square_side_length = getGrid(screenshot)
    mask = np.zeros(screenshot.shape[:2], np.uint8)
    x = gridArray[column, row, 0]
    y = gridArray[column, row, 1]
    cv.rectangle(mask, (x, y), (x+square_side_length, y+square_side_length), color=(255, 255, 255), thickness=cv.FILLED)
    field_img = cv.bitwise_and(screenshot,screenshot,mask = mask)
    cv.imshow('Field',field_img)
    cv.waitKey(0)




def getEmojiCenterPoint(screenshot):

    game_image = getGameImage(screenshot)
    game_image_hsv = cv.cvtColor(game_image, cv.COLOR_BGR2HSV)
    #I'm detecting Emoji based on yellow color
    lower_threshold = np.array([10, 0, 230])
    upper_threshold = np.array([31, 255, 255])
    emoji_mask = cv.inRange(game_image_hsv, lower_threshold, upper_threshold)
    cv.dilate(emoji_mask, kernel=np.ones((5, 5), np.uint8))
    emoji_contours, _ = cv.findContours(emoji_mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    emoji_contours = sorted(emoji_contours, key=cv.contourArea, reverse=True)
    M = cv.moments(emoji_contours[0])
    x_center = int(M["m10"] / M["m00"])
    y_center = int(M["m01"] / M["m00"])
    
    return x_center, y_center
    #pyautogui.click(x, y)




def getGameImage(screenshot):

    hsv = cv.cvtColor(screenshot, cv.COLOR_BGR2HSV)
    #I'm detecting the game area based on certain shades of gray with no vibrance
    lower_threshold = np.array([0, 0, 130])
    upper_threshold = np.array([0, 0, 200])
    game_mask = cv.inRange(hsv, lower_threshold, upper_threshold)
    game_mask = cv.morphologyEx(game_mask, cv.MORPH_OPEN, kernel=np.ones((3,3), np.uint8))
    game_contours, _ = cv.findContours(game_mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    rectangle_contours = filterRectangleContours(game_contours)
    game_mask = np.zeros((screenshot.shape[:2]), np.uint8)
    #I'm assuming the biggest contour is bounding the game area
    rec_contours = sorted(rectangle_contours, key=cv.contourArea, reverse=True)
    cv.drawContours(game_mask, [rectangle_contours[0]], -1, color=(255, 255, 255), thickness=cv.FILLED)
    
    return cv.bitwise_and(screenshot, screenshot, mask=game_mask)



def filterRectangleContours(contours):
    rectangle_contours = []
    for cnt in contours:
        approx = cv.approxPolyDP(cnt, 0.02*cv.arcLength(cnt, True), True)
        if len(approx) == 4:
            rectangle_contours.append(cnt)

    return rectangle_contours



def drawContours(image, contours):
    for cnt in contours:
        cv.drawContours(image, contours, 3, (0,255,0), 3)
    
    cv.imshow("contours", image)
    cv.waitKey(0)