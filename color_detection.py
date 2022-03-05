import cv2
import numpy as np
from config import *

# Grid
cell_size = [
    (corners[1][0]-corners[0][0]) // grid_size[0],
    (corners[1][1]-corners[0][1]) // grid_size[1]
]

def bgr_to_hsv(color):
    arr = np.uint8([[list(color)]])
    r, g, b = cv2.cvtColor(arr, cv2.COLOR_BGR2HSV)[0][0]
    return [r, g, b]

def hsv_to_bgr(color):
    arr = np.uint8([[list(color)]])
    r, g, b = cv2.cvtColor(arr, cv2.COLOR_HSV2BGR)[0][0]
    return [r, g, b]

emoji = {
    "W":"⚫",
    " ":"⚪",
    "C":"🟢",
    "M":"🟡"
}

def detect(img):
    colors = [["" for _ in range(grid_size[0])] for _ in range(grid_size[1])]
    for y in range(grid_size[1]):
        for x in range(grid_size[0]):
            mx = corners[0][0] + x * cell_size[0]
            my = corners[0][1] + y * cell_size[1]

            cv2.rectangle(img, (mx, my), (mx+cell_size[0], my+cell_size[1]), color=(0, 0, 255), thickness=2)
            mean_color = np.array(bgr_to_hsv(cv2.mean(img[my:my+cell_size[0], mx:mx+cell_size[0]])[:-1]))
            
            # cv2.imshow("cropped", img[my:my+cell_size[0], mx:mx+cell_size[0]])
            # print(mean_color)
            # cv2.waitKey()
            
            diffs = [
                np.linalg.norm(mean_color - GREY),
                np.linalg.norm(mean_color - WHITE),
                np.linalg.norm(mean_color - GREEN),
                np.linalg.norm(mean_color - YELLOW)
            ]
            min_diff = min(diffs)
            min_index = diffs.index(min_diff)
            best_color = ["W"," ","C","M"][min_index]

            colors[y][x] = best_color
    return colors

def printGrid(colors):
    print("\n".join(["".join([emoji[i] for i in row]) for row in colors]))

if __name__ == "__main__":
    img = cv2.imread('dewarped.png')
    print(colors)
    printGrid()
    cv2.imshow('color grid', img)
    cv2.waitKey()