import cv2 as cv2
import numpy as np
from anki_object_detection.cube import Cube


class CubeDetector:

    # define range of blue color in HLS
    LOWER_BLUE = np.array([100, 70, 120])
    UPPER_BLUE = np.array([125, 178, 255])

    def __init__(self, lower_color_range=LOWER_BLUE, upper_color_range=UPPER_BLUE):
        super()
        self.lower_color_range = lower_color_range
        self.upper_color_range = upper_color_range

    def detect(self, frame):
        image_height, image_width, channels = frame.shape

        # Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)

        # Threshold the HSV image to get only blue colors
        mask = cv2.inRange(hsv, self.lower_color_range, self.upper_color_range)
        im2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        biggest_contour_size = 0
        biggest_contour = None

        min_object_height = image_height * 0.02
        min_object_width = image_width * 0.02
        # Find the biggest contour in the center
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)

            if w > min_object_width and h > min_object_height:
                aspect_ratio = w / h

                # Allow rectangles that have double height
                if aspect_ratio < 1.2 and aspect_ratio >= 0.5:
                    if w*h > biggest_contour_size:
                        biggest_contour_size = w*h
                        biggest_contour = cnt

        x, y, w, h = cv2.boundingRect(biggest_contour)

        #cv2.drawContours(frame, contours, -1, (255, 255, 0), 3)
        #cv2.rectangle(frame, (x,y), (x+w, y+h), (255, 0, 0), 3)
        #cv2.namedWindow('test', cv2.WINDOW_NORMAL)
        #cv2.imshow('test', frame)
        #cv2.waitKey(0)
        return Cube(x, y, w, h)
