import cv2 as cv
import numpy as np
import imutils


ss = cv.imread('ss2.png',-1)

lower = np.array([130, 130, 130, 0])
upper = np.array([200, 200, 200, 255])

game_mask = cv.inRange(ss, lower, upper)
kernel = np.ones((3, 3), np.uint8)
game_mask = cv.erode(game_mask, kernel) 

cv.imshow("game_mask", game_mask)
cv.waitKey(0)

game_contours, _ = cv.findContours(game_mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

areas = []
for i in game_contours:
    area = cv.contourArea(i)
    areas.append(area)

sortedContours = sorted(game_contours, key=cv.contourArea, reverse=True)

field_mask = np.zeros((game_mask.shape),np.uint8)
cv.drawContours(field_mask, [sortedContours[1]], -1, color=(255, 255,255), thickness=cv.FILLED)
field_mask = cv.bitwise_and(cv.bitwise_not(game_mask), cv.bitwise_not(game_mask), mask=field_mask)
cv.imshow("field_mask", field_mask)
cv.waitKey(0)

#for sc in sortedContours:
#    cv.drawContours(ss, [sc], -1, (0,0,255), 2)
#    cv.imshow("ss", ss)
#    cv.waitKey(0)

for cnt in game_contours:
   approx = cv.approxPolyDP(cnt, 0.02*cv.arcLength(cnt, True), True)
   if len(approx) == 4:
      x, y, w, h = cv.boundingRect(cnt)
      ratio = float(w)/h
      if ratio >= 0.9 and ratio <= 1.1:
         ss = cv.drawContours(ss, [cnt], -1, (0,255,255), 2)
      else:
         ss = cv.drawContours(ss, [cnt], -1, (0,0,255), 2)

cv.imshow("Shapes", ss)
cv.waitKey(0)