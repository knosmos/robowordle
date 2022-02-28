import cv2
import numpy as np
from rich import print

image = cv2.imread('printed2.png')

SIZE = 600

# Get ROI corners

arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_APRILTAG_36h11)
arucoParams = cv2.aruco.DetectorParameters_create()
(corners, ids, rejected) = cv2.aruco.detectMarkers(image, arucoDict, parameters=arucoParams)

print(corners, ids, rejected)
assert len(corners) == len(ids) == 4

detected = [[ids[i], corners[i]] for i in range(4)]
detected.sort(key = lambda x: x[0])
print(detected)
bounding_box = [
    detected[0][1][0][2],
    detected[1][1][0][3],
    detected[2][1][0][0],
    detected[3][1][0][1]
]
print(bounding_box)

img_boxed = image.copy()
cv2.polylines(img_boxed, np.int32([bounding_box]), True, (0, 255, 0), 2)
# cv2.imshow('Fiducial Detection', img_boxed)

# Dewarp
vertices = [
    [0, 0],
    [SIZE, 0],
    [SIZE, SIZE],
    [0, SIZE]
]
matrix = cv2.getPerspectiveTransform(np.float32(bounding_box), np.float32(vertices))
dewarped = cv2.warpPerspective(image, matrix, (SIZE, SIZE))
cv2.imwrite('dewarped_2.png', dewarped)
cv2.imshow('Dewarped', dewarped)

cv2.waitKey()
cv2.destroyAllWindows()