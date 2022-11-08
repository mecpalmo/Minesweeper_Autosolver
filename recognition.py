import cv2 as cv
import numpy as np
import imutils

ss = cv.imread('ss2.png',-1)

lower = np.array([130, 130, 130, 0])
upper = np.array([200, 200, 200, 255])

mask = cv.inRange(ss, lower, upper)

contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

areas = []
for i in contours:
    area = cv.contourArea(i)
    areas.append(area)

sortedContours = sorted(contours, key=cv.contourArea, reverse=True)

for sc in sortedContours:
    cv.drawContours(ss, [sc], -1, (0,0,255), 3)
    cv.waitKey(0)
    cv.imshow("ss",ss)

cv.waitKey(0)