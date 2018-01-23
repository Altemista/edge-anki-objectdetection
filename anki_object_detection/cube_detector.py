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

    def detect(self, frame, max_left_lane, max_right_lane, max_upper_lane, max_lower_lane):
        cropped_vertical_image = frame[max_left_lane.y1:max_right_lane.y2, max_left_lane.x1:max_right_lane.x2]

        cube_vertical = self.detect_in_area(cropped_vertical_image, frame, max_left_lane.x1, max_left_lane.y1)
        if cube_vertical.x != 0 and cube_vertical.y != 0:
            return Cube(cube_vertical.x + max_left_lane.x1, cube_vertical.y + max_left_lane.y1, cube_vertical.width, cube_vertical.height)
        else:
            cropped_horizontal_image = frame[max_upper_lane.y1:max_lower_lane.y2, max_upper_lane.x1:max_lower_lane.x2]
            cube_horizontal = self.detect_in_area(cropped_horizontal_image, frame, max_upper_lane.x1, max_upper_lane.y1)
            return Cube(cube_horizontal.x + max_upper_lane.x1, cube_horizontal.y + max_upper_lane.y1, cube_horizontal.width, cube_horizontal.width)

    def detect_in_area(self, image, frame, offset_x, offset_y):
        image_height, image_width, channels = image.shape

        # Convert BGR to HSV
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)

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
                if w*h > biggest_contour_size:
                    biggest_contour_size = w*h
                    biggest_contour = cnt

        x, y, w, h = cv2.boundingRect(biggest_contour)

        cv2.drawContours(frame, contours, -1, (255, 255, 0), 3, offset=(offset_x, offset_y))
        return Cube(x, y, w, h)
