import cv2 as cv
import image_processing as ip

TESTING = False

def getTestImage(index):
    image = cv.imread(f'ss{index}.png',-1)
    image = cv.cvtColor(image, cv.COLOR_BGRA2BGR)
    return image


if(TESTING):
    print("test 1")
    _, _, columns, rows, _ = ip.getGridDetails(getTestImage(1))
    print(f"Grid: {columns}x{rows}, Should be: 30x16")

    print("test 2")
    _, _, columns, rows, _ = ip.getGridDetails(getTestImage(2))
    print(f"Grid: {columns}x{rows}, Should be: 30x16")

    print("test 3")
    _, _, columns, rows, _ = ip.getGridDetails(getTestImage(3))
    print(f"Grid: {columns}x{rows}, Should be: 9x9")

    print("test 4")
    _, _, columns, rows, _ = ip.getGridDetails(getTestImage(4))
    print(f"Grid: {columns}x{rows}, Should be: 9x9")

    print("test 5")
    _, _, columns, rows, _ = ip.getGridDetails(getTestImage(5))
    print(f"Grid: {columns}x{rows}, Should be: 30x16")