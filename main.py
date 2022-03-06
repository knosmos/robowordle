import cv2
import numpy as np
import time

from config import *
import printer_control
import dewarp
import color_detection
# import camera
import solver

# camera.start()
print("starting camera...")
cap = cv2.VideoCapture(2)
time.sleep(2)
cap.set(15, EXPOSURE)

def run():
    opt = "sauce" # nonoptimal starter word is used to make the game longer
    result = ""
    num_guesses = 0
    printer_control.home()
    printer_control.ready_position()
    while num_guesses != 3: #result != ["C","C","C","C","C"]: <- in future it will detect completion (the stats page shows up preventing final)
        try:
            print(f"guessing [{opt}]")
            printer_control.typeWord(opt)
            print("waiting for result...")
            time.sleep(10) # In case printer hasn't stopped moving

            ret, frame = cap.read()
            frame = dewarp.dewarp(frame)
            # cv2.imshow("frame", frame)
            # cv2.waitKey()
            color_grid = color_detection.detect(frame) # camera.current_img)
            print("Detected colors:")
            color_detection.printGrid(color_grid)
            result = color_grid[num_guesses]

            solver.words = solver.reduce(opt, result)
            opt = ""
            opt_size = float("inf")
            for word in solver.words:
                p = solver.partition(word)
                avg_partition_size = sum(p)/len(p)
                if opt_size > avg_partition_size:
                    opt_size = avg_partition_size
                    opt = word
            num_guesses += 1       
        except KeyboardInterrupt:
            # printer_control.disconnect()
            break
    print("the answer is", opt)
    printer_control.set_pos(y=200)
    printer_control.disconnect()

if __name__ == "__main__":
    run()