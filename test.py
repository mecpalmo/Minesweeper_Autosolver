import cv2 as cv

def getTestImage(index):
    image = cv.imread(f'ss{index}.png',-1)
    image = cv.cvtColor(image, cv.COLOR_BGRA2BGR)
    return image
