import cv2 as cv2
import numpy as np
from anki_object_detection.cube import  Cube


class CubeDetector:

    # define range of blue color in HSV
    LOWER_BLUE = np.array([80, 70, 70])
    UPPER_BLUE = np.array([130, 255, 255])

    def __init__(self):
        super()

    def detect(self, frame):
        # Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Threshold the HSV image to get only blue colors
        mask = cv2.inRange(hsv, self.LOWER_BLUE, self.UPPER_BLUE)

        im2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        biggest_contour_size = 0
        biggest_contour = None

        # Find the biggest contour
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            if w*h > biggest_contour_size:
                biggest_contour_size = w*h
                biggest_contour = cnt

        x, y, w, h = cv2.boundingRect(biggest_contour)
        return Cube(x, y, w, h)
