import screen_reader as sr
import cv2 as cv

ss = cv.imread('ss2.png',-1)
ss = cv.cvtColor(ss, cv.COLOR_BGRA2BGR)

#ss = getScreenshot()

sr.getFieldImage(ss,2,3)

#print(sr.getEmojiCenterPoint(ss))