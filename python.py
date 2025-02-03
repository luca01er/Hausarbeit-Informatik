from ppadb.client import Client
import pyautogui
import numpy as np
import cv2 as cv

adb = Client(host="127.0.0.1", port=5037)
devices = adb.devices()

if len(devices) == 0:
    print("No Device attached")
    quit()

device = devices[0]

image = device.screencap()

with open("screen.png", "wb") as fp:
    fp.write(image)

screenshot = image

screen = cv.imread("screen.png", cv.IMREAD_UNCHANGED)
game = cv.imread("Game.png", cv.IMREAD_UNCHANGED)

w = game.shape[1]
h = game.shape[0]

result = cv.matchTemplate(screen, game, cv.TM_CCOEFF_NORMED)

min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

threshold = .65

yloc, xloc = np.where(result >= threshold)



rectangles = []
for (x, y) in zip(xloc, yloc):
    rectangles.append([int(x), int(y), int(w), int(h)])

rectangles, weights = cv.groupRectangles(rectangles, 1, 0.2)

for (x, y, w, h) in (rectangles):
    cv.rectangle(screen, (x, y), (x + w, y + h), (0,255,255), 2)

print(len(rectangles))

device.shell("input tap {} {}".format(x,y))


cv.imshow("Result", screen)
#cv.imshow("Game", result)

cv.waitKey(0)

cv.destroyAllWindows()
