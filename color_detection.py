import cv2
import numpy as np

# Grid
corners = [(227, 167), (373, 343)]
grid_size = (5, 6)
cell_size = [
    (corners[1][0]-corners[0][0]) // grid_size[0],
    (corners[1][1]-corners[0][1]) // grid_size[1]
]

# Colors
GREY = np.array([98, 100, 127])
WHITE = np.array([170, 164, 184])
GREEN = np.array([72, 125, 105])
YELLOW = np.array([67, 130, 162])

emoji = {
    "W":"⚫",
    " ":"⚪",
    "C":"🟢",
    "M":"🟡"
}

colors = [["" for _ in range(grid_size[0])] for _ in range(grid_size[1])]

img = cv2.imread('dewarped_2.png')
for y in range(grid_size[1]):
    for x in range(grid_size[0]):
        mx = corners[0][0] + x * cell_size[0]
        my = corners[0][1] + y * cell_size[1]

        cv2.rectangle(img, (mx, my), (mx+cell_size[0], my+cell_size[1]), color=(0, 0, 255), thickness=2)
        mean_color = np.array(cv2.mean(img[my:my+cell_size[0], mx:mx+cell_size[0]])[:-1])
        
        #cv2.imshow("cropped", img[my:my+cell_size[0], mx:mx+cell_size[0]])
        #print(mean_color)
        #cv2.waitKey()
        
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
print(colors)
print("\n".join(["".join([emoji[i] for i in row]) for row in colors]))

cv2.imshow('color grid', img)
cv2.waitKey()