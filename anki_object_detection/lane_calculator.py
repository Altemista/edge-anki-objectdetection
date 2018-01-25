import cv2 as cv2
from anki_object_detection.line import Line


class LaneCalculator:
    @staticmethod
    def _calculate_vertical_lane(left_x, right_x, cube_x, frame):
        laneNo = -1
        laneWidth = (right_x-left_x) / 4
        if cube_x < left_x+laneWidth:
            laneNo = 1
        elif left_x < cube_x < left_x+laneWidth*2:
            laneNo = 2
        elif left_x < cube_x < left_x+laneWidth*3:
            laneNo = 3
        elif left_x < cube_x:
            laneNo = 4

        # print separator lanes
        height, width, channels = frame.shape
        cv2.line(frame, (int(left_x), 0), (int(left_x), width), (0, 255, 0), 2)
        cv2.line(frame, (int(left_x+laneWidth), 50), (int(left_x+laneWidth), width), (0, 255, 0), 2)
        cv2.line(frame, (int(left_x+laneWidth*2), 50), (int(left_x+laneWidth*2), width), (0, 255, 0), 2)
        cv2.line(frame, (int(left_x+laneWidth*3), 50), (int(left_x+laneWidth*3), width), (0, 255, 0), 2)
        cv2.line(frame, (int(left_x+laneWidth*4), 50), (int(left_x+laneWidth*4), width), (0, 255, 0), 2)

        return laneNo

    @staticmethod
    def _calculate_horizontal_lane(upper_y, lower_y, cube_y, frame):
        laneNo = -1
        laneHeight = (lower_y-upper_y) / 4
        if cube_y < upper_y+laneHeight:
            laneNo = 1
        elif upper_y < cube_y < upper_y+laneHeight*2:
            laneNo = 2
        elif upper_y < cube_y < upper_y+laneHeight*3:
            laneNo = 3
        elif upper_y < cube_y:
            laneNo = 4

        # print separator lanes
        height, width, channels = frame.shape
        cv2.line(frame, (0, int(upper_y)), (height, int(upper_y)), (0, 255, 0), 2)
        cv2.line(frame, (0, int(upper_y+laneHeight)), (height, int(upper_y+laneHeight)), (0, 255, 0), 2)
        cv2.line(frame, (0, int(upper_y+laneHeight*2)), (height, int(upper_y+laneHeight*2)), (0, 255, 0), 2)
        cv2.line(frame, (0, int(upper_y+laneHeight*3)), (height, int(upper_y+laneHeight*3)), (0, 255, 0), 2)
        cv2.line(frame, (0, int(upper_y+laneHeight*4)), (height, int(upper_y+laneHeight*4)), (0, 255, 0), 2)

        return laneNo

    @staticmethod
    def get_lane_for_cube(frame, cube, max_left_lane, max_right_lane, max_horizontal_upper_lane, max_horizontal_lower_lane):

        cv2.rectangle(frame, (cube.x, cube.y), (cube.x+cube.width, cube.y+cube.height), (255, 0, 0), 2)
        if max_left_lane is not None and max_right_lane is not None:

            mean_upper_y = (max_horizontal_upper_lane.y1+max_horizontal_upper_lane.y2)/2
            mean_lower_y = (max_horizontal_lower_lane.y1+max_horizontal_lower_lane.y2)/2
            mean_right_x = (max_right_lane.x1+max_right_lane.x2)/2
            mean_left_x = (max_left_lane.x1+max_left_lane.x2)/2

            # Cube.y is upper corner
            cube_y = cube.y + cube.height
            cube_x = cube.x + cube.width / 2

            # A crossing can be split into 5 parts
            vertical_lane = -1
            horizontal_lane = -1

            # vertical upper, horizontal middle (implicit)
            if cube_y < mean_upper_y*0.9:
                #print("DEBUG: Cube in vertical upper, horizontal middle part(not affected)")
                vertical_lane = LaneCalculator._calculate_vertical_lane(max_left_lane.x1, max_right_lane.x1, cube_x, frame)
            # vertical lower, horizontal middle (implicit)
            elif cube_y > mean_lower_y*1.1:
                #print("DEBUG: Cube in vertical lower, horizontal middle part(not affected)")
                vertical_lane = LaneCalculator._calculate_vertical_lane(max_left_lane.x2, max_right_lane.x2, cube_x, frame)
            # vertical middle, horizontal left
            elif cube_x < mean_left_x:
                #print("DEBUG: Cube in vertical middle(not affected), horizontal left part")
                horizontal_lane = LaneCalculator._calculate_horizontal_lane(max_horizontal_upper_lane.y1, max_horizontal_lower_lane.y1, cube_y, frame)
            # vertical middle, horizontal right
            elif cube_x > mean_right_x:
                #print("DEBUG: Cube in vertical middle(not affected), horizontal right part")
                horizontal_lane = LaneCalculator._calculate_horizontal_lane(max_horizontal_upper_lane.y2, max_horizontal_lower_lane.y2, cube_y, frame)
            # vertical middle, horizontal middle
            else:
                #print("DEBUG: Cube in vertical middle, horizontal middle part")
                vertical_lane = LaneCalculator._calculate_vertical_lane(mean_left_x, mean_right_x, cube.x+cube.width/2, frame)
                horizontal_lane = LaneCalculator._calculate_horizontal_lane(mean_upper_y, mean_lower_y, cube_y, frame)

            # print lanes
            cv2.line(frame, (max_left_lane.x1, max_left_lane.y1), (max_left_lane.x2, max_left_lane.y2), (255, 0, 0), 5)
            cv2.line(frame, (max_right_lane.x1, max_right_lane.y1), (max_right_lane.x2, max_right_lane.y2), (255, 0, 0), 5)
            cv2.line(frame, (max_horizontal_upper_lane.x1, max_horizontal_upper_lane.y1), (max_horizontal_upper_lane.x2, max_horizontal_upper_lane.y2), (255, 0, 0), 5)
            cv2.line(frame, (max_horizontal_lower_lane.x1, max_horizontal_lower_lane.y1), (max_horizontal_lower_lane.x2, max_horizontal_lower_lane.y2), (255, 0, 0), 5)

            return vertical_lane, horizontal_lane
        return -1