import cv2 as cv2
import numpy as np
import math
from anki_object_detection.line import Line


class LaneDetector():
    LOWER_ORANGE = np.array([10, 150, 150], dtype="uint8")
    UPPER_ORANGE = np.array([20, 255, 255], dtype="uint8")

    def detect(self, frame):

        # image = cv2.imread('images/lanes2.jpg')
        # gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        mask_yellow = cv2.inRange(hsv_image, self.LOWER_ORANGE, self.UPPER_ORANGE)
        mask_yellow = cv2.GaussianBlur(mask_yellow, (15, 15), 0)

        # Apply canny edge to yellow masked image
        edge_image = cv2.Canny(mask_yellow, 0, 255)

        # get all lines with a hough transform
        lines = cv2.HoughLinesP(edge_image, rho=1, theta=np.pi/180, threshold=20, minLineLength=20, maxLineGap=300)

        # if we did not find any lines, return none
        if lines is None:
            return None, None

        interpolated_lines = self._interpolate_vetical_lines(lines, 10)

        self._plot_lines(interpolated_lines, mask_yellow)

        return self._get_lanes(interpolated_lines)

    def _unit_vector(self, vector):
        """ Returns the unit vector of the vector.  """
        return vector / np.linalg.norm(vector)

    def _calc_angle(self, v1):
        """ Returns the angle in radians between vectors 'v1' and 'basis horizontal vector':
        """
        v1_u = self._unit_vector(v1)
        v2_u = self._unit_vector((1, 0))

        angle = np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))
        #print(angle * (180/math.pi))

        #image = np.zeros((500,500,3), np.uint8)
        #cv2.line(image, (250, 500), (int(250+v1_u[0]*250), int(500-v1_u[1]*500)), (255, 0, 0), 5)
        #cv2.line(image, (250, 500), (int(250+v2_u[0]*250), int(500-v2_u[1]*500)), (255, 0, 0), 5)

        #cv2.namedWindow('test', cv2.WINDOW_NORMAL)
        #cv2.imshow('test', image)
        #cv2.waitKey(0)

        return angle * (180/math.pi)

    def _interpolate_vetical_lines(self, lines, threshold=10):
        """ Returns all the aggregated vertical lines that point to the same direction
        :param self: 
        :param lines: The lines found with hough transform
        :param threshold: Direction threshold for aggregating same lines
        :return: 
        """
        interpolated_lines = {}
        # interpolate lines by aggregating all the vertical lines that point in the same direction (+, - threshold
        for line in lines:
            for x1, y1, x2, y2 in line:

                # swap orientation if line goes bottom up (not up down)
                if y1 > y2:
                    x1, x2, y1, y2 = self._swap_line_orientation(x1, x2, y1, y2)

                # calculate the angle
                angle = int(self._calc_angle((x2 - x1, y2 - y1)))

                # ignore lines that do not point vertically
                if angle < 110 and angle > 80:
                    print(angle)
                    closest_line = None
                    for keyAngle in interpolated_lines:
                        if abs(keyAngle-angle) < threshold:
                            closest_line = interpolated_lines[keyAngle]

                            if closest_line.in_area(x1, x2, y1, y2):
                                # Calculate x values (for horizontally aligned lines)
                                if closest_line.y1 > y1:
                                    closest_line.x1 = x1

                                if closest_line.y2 < y2:
                                    closest_line.x2 = x2

                                closest_line.y1 = min(y1, closest_line.y1)
                                closest_line.y2 = max(y2, closest_line.y2)
                                break

                    if closest_line is None:
                        interpolated_lines[angle] = Line(x1, x2, y1, y2)

        return interpolated_lines

    def _swap_line_orientation(self, x1, x2, y1, y2):
        """
        A line should point bottom-up, swap if its top-down
        :param x1: 
        :param x2: 
        :param y1: 
        :param y2: 
        :return: 
        """
        y1_copy = y1
        y1 = y2
        y2 = y1_copy
        x1_copy = x1
        x1 = x2
        x2 = x1_copy
        return x1, x2, y1, y2

    def _get_lanes(self, interpolated_lines):
        """
        Calculates the most outer lines
        :param interpolated_lines: 
        :return: 
        """
        max_left_lane = None
        max_right_lane = None

        for line in interpolated_lines.values():

            line_height = abs(line.y1-line.y2)

            # prune too short lines < 50 pixels
            if line_height < 50:
                continue

            # init
            if max_left_lane is None:
                max_left_lane = line
                max_right_lane = line
            else:
                # if line is more at the left than max_left_lane
                if line.x1-max_left_lane.x1 < -50 or line.x2-max_left_lane.x2 < -50:
                    max_left_lane = line
                elif line.x1-max_right_lane.x1 > 50 or line.x2-max_right_lane.x2 > 50:
                    max_right_lane = line

        return max_left_lane, max_right_lane

    def _plot_lines(self, lines, image):
        for line in lines.values():
            cv2.line(image, (line.x1, line.y1), (line.x2, line.y2), (255, 0, 0), 5)

        #cv2.namedWindow('test', cv2.WINDOW_NORMAL)
        #cv2.imshow('test', image)
        #cv2.waitKey(0)