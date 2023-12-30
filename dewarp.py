import cv2, time
import numpy as np

SIZE = 600

# Get ROI corners
#arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_APRILTAG_36h11)
#arucoParams = cv2.aruco.DetectorParameters_create()

dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_APRILTAG_36h11)
parameters = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(dictionary, parameters)

def white_balance(img):
    result = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    avg_a = np.average(result[:, :, 1])
    avg_b = np.average(result[:, :, 2])
    result[:, :, 1] = result[:, :, 1] - ((avg_a - 128) * (result[:, :, 0] / 255.0) * 1.1)
    result[:, :, 2] = result[:, :, 2] - ((avg_b - 128) * (result[:, :, 0] / 255.0) * 1.1)
    result = cv2.cvtColor(result, cv2.COLOR_LAB2BGR)
    return result

# custom color balancer

def white_balance2(img):
    result = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    avg_a = np.average(result[150:500, 0:150, 1])
    avg_b = np.average(result[150:500, 0:150, 2])
    result[:, :, 1] = result[:, :, 1] - ((avg_a - 128) * (result[:, :, 0] / 255.0) * 1.1)
    result[:, :, 2] = result[:, :, 2] - ((avg_b - 128) * (result[:, :, 0] / 255.0) * 1.1)
    result = cv2.cvtColor(result, cv2.COLOR_LAB2BGR)
    return result

'''
def white_balance2(img):
    # get white rect
    rect = img[150:500, 0:150]
    cv2.imshow('rect', rect)
    cv2.waitKey()
    avg_color = np.average(rect, axis=(0,1))
    lum = np.average(avg_color)
    # apply offsets
    img[:,:,0] = img[:,:,0] * (lum / avg_color[0])
    img[:,:,1] = img[:,:,1] * (lum / avg_color[1])
    img[:,:,2] = img[:,:,2] * (lum / avg_color[2])
    return img
'''
def dewarp(img):
    # cv2.imshow('Original', img)
    # cv2.waitKey()
    #(corners, ids, rejected) = cv2.aruco.detectMarkers(img, arucoDict, parameters=arucoParams)
    (corners, ids, rejected) = detector.detectMarkers(img)

    # print(corners, ids, rejected)
    assert len(corners) == len(ids) == 4

    detected = [[ids[i], corners[i]] for i in range(4)]
    detected.sort(key = lambda x: x[0])
    # print(detected)
    bounding_box = [
        detected[0][1][0][2],
        detected[1][1][0][3],
        detected[2][1][0][0],
        detected[3][1][0][1]
    ]
    # print(bounding_box)

    img_boxed = img.copy()
    cv2.polylines(img_boxed, np.int32([bounding_box]), True, (0, 255, 0), 2)
    # cv2.imshow('Fiducial Detection', img_boxed)

    # Dewarp
    vertices = [
        [0, 0],
        [SIZE, 0],
        [SIZE, SIZE],
        [0, SIZE]
    ]
    print(vertices)
    matrix = cv2.getPerspectiveTransform(np.float32(bounding_box), np.float32(vertices))
    dewarped = cv2.warpPerspective(img, matrix, (SIZE, SIZE))
    #cv2.imshow('Dewarped', dewarped)
    return white_balance2(dewarped)

if __name__ == "__main__":
    #cap = cv2.VideoCapture(2)
    cap = cv2.VideoCapture(2, cv2.CAP_DSHOW) # this is the magic!

    #cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    #cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    #time.sleep(2)
    cap.set(15, -5.5)
    ret, img = cap.read()
    cv2.imshow('Original', img)
    cv2.waitKey()
    # img = cv2.imread('img/setupTest.jpg')
    dewarped = dewarp(img)

    cv2.imwrite('dewarped.png', dewarped)
    cv2.imshow('Dewarped_w', dewarped)

    cv2.waitKey()
    cv2.destroyAllWindows()
    '''
    img = cv2.imread('de_0.png')
    dewarped = white_balance(img)
    cv2.imshow('Dewarped_w', dewarped)
    cv2.waitKey()
    '''