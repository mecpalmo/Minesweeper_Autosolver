import screen_reader as sr
import cv2 as cv

ss = cv.imread('ss2.png',-1)
ss = cv.cvtColor(ss, cv.COLOR_BGRA2BGR)

#ss = getScreenImage()

sr.getFieldImage(ss,0,0)