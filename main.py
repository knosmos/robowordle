import cv2
import numpy as np
import time

from config import *
import printer_control
import dewarp
import color_detection
import camera
from solver import reduce, partition

camera.start()

def run():
    opt = "crate"
    result = ""
    num_guesses = 0
    while result != "CCCCC":
        print("guessing", opt)
        printer_control.typeWord(opt)
        print("waiting for result...")
        time.sleep(2) # In case printer hasn't stopped moving
        result = color_detection.detect(camera.current_img)[num_guesses]

        words = reduce(opt, result, words)
        opt = ""
        opt_size = float("inf")
        for word in words:
            p = partition(word, words)
            avg_partition_size = sum(p)/len(p)
            if opt_size > avg_partition_size:
                opt_size = avg_partition_size
                opt = word
        num_guesses += 1
    print("the answer is", opt)