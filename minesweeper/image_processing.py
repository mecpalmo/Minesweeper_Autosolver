import cv2 as cv
import numpy as np
from field_enum import Field_Content

SHOW_GRID_RECOGNITION = False

columns_table = []
rows_table = []

def getGridDetails(screenshot):
    game_image = getGameImage(screenshot)
    game_image_gray = cv.cvtColor(game_image, cv.COLOR_BGR2GRAY)
    game_mask = cv.inRange(game_image_gray, 130, 200)
    game_mask = cv.morphologyEx(game_mask, cv.MORPH_CLOSE, kernel=np.ones((3,3), np.uint8))
    game_mask = cv.morphologyEx(game_mask, cv.MORPH_OPEN, kernel=np.ones((3,3), np.uint8))
    game_contours, _ = cv.findContours(game_mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    rectangle_contours = filterRectangleContours(game_contours)
    rectangle_contours = sorted(rectangle_contours, key=cv.contourArea, reverse=True)
    #I'm assuming the 2nd biggest rectangle contour is around the grid
    grid_mask = np.zeros((game_image.shape[:2]), np.uint8)
    cv.drawContours(grid_mask, rectangle_contours, contourIdx=1, color=(255, 255, 255), thickness=cv.FILLED)
    #the grid mask needs to be smoothened out. We need it quite precise
    grid_mask = cv.erode(grid_mask, kernel=np.ones((11, 11), np.uint8))
    grid_mask = cv.erode(grid_mask, kernel=np.ones((11, 11), np.uint8))
    grid_image = cv.bitwise_and(game_image, game_image, mask=grid_mask)
    grid_canny = cv.Canny(grid_image,100,300,apertureSize = 3)
    grid_contours, _ = cv.findContours(grid_canny, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    square_contours = filterSquareContours(grid_contours)
    drawContours(grid_image, square_contours)
    contours_coordinate = []
    for cnt in square_contours:
        M = cv.moments(cnt)
        x_center = int(M["m10"] / M["m00"])
        contours_coordinate.append(x_center)
    #we only need one axis to find most common space between centers of neighbouring fields
    x_set = set(contours_coordinate)
    contours_coordinate = sorted(list(x_set))
    x_spaces = []
    for i in range(0, len(contours_coordinate)-1):
        x_spaces.append(contours_coordinate[i+1]-contours_coordinate[i])
    #I'm assuming the square side is equal to the biggest space between fields
    square_side_length = np.max(x_spaces)
    #we need the size of entire grid to calculate how many fields fit in
    grid_mask_contours, _ = cv.findContours(grid_mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    sorted(grid_mask_contours, reverse=True)
    #I'm assuming the biggest contour of grid_mask marks the grid
    x0, y0, width, height = cv.boundingRect(grid_mask_contours[0])
    columns = int(np.round((width)/(square_side_length)))
    rows = int(np.round((height)/(square_side_length)))
    print(f"Columns: {columns}, Rows: {rows}")
    return x0, y0, columns, rows, square_side_length


def getDefinedGrid(screenshot):
    x0, y0, columns, rows, square_side_length = getGridDetails(screenshot)
    grid_image = screenshot[y0:(y0+rows*square_side_length), x0:(x0+columns*square_side_length)]
    #showImage(grid_image)
    grid_content = np.ones((columns,rows))*Field_Content.UNDETERMINED.value
    for column in range(0,columns):
        for row in range(0,rows):
            grid_content[column, row] = classifyFieldContent(grid_image, column, row, square_side_length)
            showImage(screenshot[(y0+row*square_side_length):(y0+(row+1)*square_side_length), (x0+column*square_side_length):(x0+(column+1)*square_side_length)])
    print(f"Grid Content: {grid_content[column, row]}")
    return grid_content, x0, y0, columns, rows, square_side_length


def classifyFieldContent(grid_image, column, row, square_side_length):
    field_image = getFieldImage(grid_image, column, row, square_side_length)
    field_image_hsv = cv.cvtColor(field_image, cv.COLOR_BGR2HSV)
    lower_threshold = np.array([0, 200, 50])
    upper_threshold = np.array([180, 255, 255])
    color_mask = cv.inRange(field_image_hsv, lower_threshold, upper_threshold)
    color_pixels = np.sum(color_mask == 255)
    area = np.square(square_side_length)
    color_pixel_ratio = color_pixels/area
    if(color_pixel_ratio > 0.1): #it's a number based on high amount of coloured pixels
        return classifyNumber(cv.bitwise_and(field_image, field_image, mask=color_mask))
    elif(color_pixel_ratio > 0): #it's a flag based on low amount of coloured pixels
        return Field_Content.CLOSED_FLAG.value
    else:
        field_image_gray = cv.cvtColor(field_image, cv.COLOR_BGR2GRAY)
        black_pixels = np.sum(field_image_gray < 5)
        black_pixel_ratio = black_pixels/area
        if(black_pixel_ratio > 0.15):
            return Field_Content.OPEN_MINE.value
        else:
            gray_pixels = np.count_nonzero((field_image_gray >= 195) & (field_image_gray <= 201))
            gray_pixel_ratio = gray_pixels/area
            if(gray_pixel_ratio > 0.70):
                return Field_Content.OPEN_EMPTY.value
            else:
                return Field_Content.CLOSED_UNKNOWN.value


def classifyNumber(image):
    image_hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    pixel = getDominantColorPixel(image_hsv)
    hue = pixel[0]
    vibration = pixel[2]
    if(vibration > 230):
        if(hue in range(115,126)): return 1
        if(hue > 175 or hue < 5): return 3
        else: pass
    elif(vibration in range(100,151)):
        if(hue in range(55,66)): return 2
        if(hue in range(115,126)): return 4
        if(hue > 175 or hue < 5): return 5 
        if(hue in range(85,96)): return 6
        if(hue in range(145,156)): return 7
        else: pass
    else: pass
    return Field_Content.UNDETERMINED.value


def getDominantColorPixel(image_hsv):
    width = image_hsv.shape[1]
    height = image_hsv.shape[0]
    pixels_of_interest = []
    for i in range(0,width):
        for j in range(0,height):
            pixel = image_hsv[i,j]
            if(pixel[2]>50):
                pixels_of_interest.append(pixel)
                return pixel #returns pixel in hsv


def getFieldImage(grid_image, column, row, square_side_length):
    mask = np.zeros(grid_image.shape[:2], np.uint8)
    x1, y1, x2, y2 = getFieldCoordinates(square_side_length, column, row)
    field_img = grid_image[y1:y2, x1:x2]
    return(field_img)


def getFieldCoordinates(square_side_length, column, row):
    x1 = column*square_side_length
    y1 = row*square_side_length
    x2 = x1 + square_side_length
    y2 = y1 + square_side_length
    return x1, y1, x2, y2


def getEmojiCenterPoint(screenshot):
    game_image = getGameImage(screenshot)
    game_image_hsv = cv.cvtColor(game_image, cv.COLOR_BGR2HSV)
    #I'm detecting Emoji based on yellow color
    lower_threshold = np.array([10, 0, 230])
    upper_threshold = np.array([31, 255, 255])
    emoji_mask = cv.inRange(game_image_hsv, lower_threshold, upper_threshold)
    emoji_mask = cv.dilate(emoji_mask, kernel=np.ones((5, 5), np.uint8))
    emoji_contours, _ = cv.findContours(emoji_mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    emoji_contours = sorted(emoji_contours, key=cv.contourArea, reverse=True)
    M = cv.moments(emoji_contours[0])
    x_center = int(M["m10"] / M["m00"])
    y_center = int(M["m01"] / M["m00"])
    return x_center, y_center


def getGameImage(screenshot):
    hsv = cv.cvtColor(screenshot, cv.COLOR_BGR2HSV)
    #I'm detecting the game area based on certain shades of gray with no vibrance
    lower_threshold = np.array([0, 0, 130])
    upper_threshold = np.array([0, 0, 200])
    game_mask = cv.inRange(hsv, lower_threshold, upper_threshold)
    game_mask = cv.morphologyEx(game_mask, cv.MORPH_CLOSE, kernel=np.ones((3,3), np.uint8))
    game_mask = cv.morphologyEx(game_mask, cv.MORPH_OPEN, kernel=np.ones((5,5), np.uint8))
    game_contours, _ = cv.findContours(game_mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    rectangle_contours = filterRectangleContours(game_contours)
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
            ratio = 0
            if(area!=0): ratio = np.square(perimeter)/area
            if(ratio > 14 and ratio < 18 and area > 25):
                square_contours.append(cnt)
    return square_contours


def drawContours(image, contours):
    image_copy = image.copy()
    cv.drawContours(image_copy, contours, -1, (0,255,0), 1)
    showImage(image_copy)


def showImage(image):
    if(SHOW_GRID_RECOGNITION):
        cv.imshow("image_function", image)
        cv.waitKey(0)