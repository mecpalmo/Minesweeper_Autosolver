import cv2 as cv
import pyautogui
import numpy as np
from collections import Counter

SHOW_IMAGE_PROCESSING = True

def getScreenshot():
    screenshot = pyautogui.screenshot()
    img = cv.cvtColor(np.array(screenshot), cv.COLOR_RGB2BGR)
    return img



def getGrid(screenshot):

    game_image = getGameImage(screenshot)
    game_image_gray = cv.cvtColor(game_image, cv.COLOR_BGR2GRAY)
    game_mask = cv.inRange(game_image_gray, 130, 200)
    game_mask = cv.morphologyEx(game_mask, cv.MORPH_CLOSE, kernel=np.ones((3,3), np.uint8))
    game_mask = cv.morphologyEx(game_mask, cv.MORPH_OPEN, kernel=np.ones((3,3), np.uint8))
    showImage(game_mask)
    game_contours, _ = cv.findContours(game_mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    rectangle_contours = filterRectangleContours(game_contours)
    rectangle_contours = sorted(rectangle_contours, key=cv.contourArea, reverse=True)
    drawContours(game_image, rectangle_contours)
    #I'm assuming the 2nd biggest rectangle contour is around the grid
    grid_mask = np.zeros((game_image.shape[:2]), np.uint8)
    cv.drawContours(grid_mask, rectangle_contours, contourIdx=1, color=(255, 255, 255), thickness=cv.FILLED)
    #the grid mask needs to be smoothened out. We need it quite precise
    grid_mask = cv.erode(grid_mask, kernel=np.ones((11, 11), np.uint8))
    grid_image = cv.bitwise_and(game_image, game_image, mask=grid_mask)
    showImage(grid_image)
    grid_canny = cv.Canny(grid_image,100,300,apertureSize = 3)
    showImage(grid_canny)
    grid_contours, _ = cv.findContours(grid_canny, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    square_contours = filterSquareContours(grid_contours)
    drawContours(grid_image, square_contours)
    
    contours_coordinate = []

    for cnt in square_contours:
        M = cv.moments(cnt)
        x_center = int(M["m10"] / M["m00"])
        contours_coordinate.append(x_center)

    #we only need one axis to find most common space between centers of neighbouring fields
    
    #make list a set to remove dupes

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
    field_img = cv.bitwise_and(screenshot, screenshot, mask=mask)
    showImage(field_img)



def getEmojiCenterPoint(screenshot):

    game_image = getGameImage(screenshot)
    game_image_hsv = cv.cvtColor(game_image, cv.COLOR_BGR2HSV)
    #I'm detecting Emoji based on yellow color
    lower_threshold = np.array([10, 0, 230])
    upper_threshold = np.array([31, 255, 255])
    emoji_mask = cv.inRange(game_image_hsv, lower_threshold, upper_threshold)
    emoji_mask = cv.dilate(emoji_mask, kernel=np.ones((5, 5), np.uint8))
    showImage(cv.bitwise_and(game_image, game_image, mask=emoji_mask))
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
    showImage(game_mask)
    game_mask = cv.morphologyEx(game_mask, cv.MORPH_CLOSE, kernel=np.ones((3,3), np.uint8))
    showImage(game_mask)
    game_mask = cv.morphologyEx(game_mask, cv.MORPH_OPEN, kernel=np.ones((5,5), np.uint8))
    showImage(game_mask)
    game_contours, _ = cv.findContours(game_mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    rectangle_contours = filterRectangleContours(game_contours)
    drawContours(screenshot, rectangle_contours)
    game_mask = np.zeros((screenshot.shape[:2]), np.uint8)
    #I'm assuming the biggest contour is bounding the game area
    rectangle_contours = sorted(rectangle_contours, key=cv.contourArea, reverse=True)
    cv.drawContours(game_mask, rectangle_contours, contourIdx=0, color=(255, 255, 255), thickness=cv.FILLED)
    return cv.bitwise_and(screenshot, screenshot, mask=game_mask)



def filterRectangleContours(contours):
    rectangle_contours = []
    for cnt in contours:
        approx = cv.approxPolyDP(cnt, 0.02*cv.arcLength(cnt, True), True)
        if len(approx) == 4:
            rectangle_contours.append(cnt)
    return rectangle_contours



def filterSquareContours(contours):
    square_contours = []
    for cnt in contours:
        approx = cv.approxPolyDP(cnt, 0.05*cv.arcLength(cnt, True), True)
        if len(approx) == 4:
            area = cv.contourArea(cnt)
            perimeter = cv.arcLength(cnt,True)
            ratio = np.square(perimeter)/area
            if(ratio > 14 and ratio < 18 and area > 9):
                square_contours.append(cnt)
    return square_contours



def drawContours(image, contours):
    image_copy = image.copy()
    cv.drawContours(image_copy, contours, -1, (0,255,0), 1)
    showImage(image_copy)



def showImage(image):
    if(SHOW_IMAGE_PROCESSING):
        cv.imshow("image_funtion", image)
        cv.waitKey(0)