import cv2 as cv2
from anki_object_detection.cube_detector import CubeDetector
from anki_object_detection.lane_calculator import LaneCalculator
from anki_object_detection.line import Line



def test_bottom_lane_1():
    cube_detector = CubeDetector()
    frame = cv2.imread("../anki_object_detection/images/cube_up_lane_1.jpg")

    max_left_lane = Line(294, 181, 68, 415)
    max_right_lane = Line(490, 654, 61, 400)
    max_horizontal_upper_lane = Line(106, 700, 130, 116)
    max_horizontal_lower_lane = Line(10, 795, 247, 223)

    cube = cube_detector.detect(frame)
    horizontal_lane, vertical_lane = LaneCalculator.get_lane_for_cube(frame, cube, max_left_lane, max_right_lane,
                                                                      max_horizontal_upper_lane, max_horizontal_lower_lane)

    assert 1 == horizontal_lane
    assert -1 == vertical_lane



def test_bottom_lane_2():
    cube_detector = CubeDetector()
    frame = cv2.imread("../anki_object_detection/images/cube_up_lane_2.jpg")

    max_left_lane = Line(294, 181, 68, 415)
    max_right_lane = Line(490, 654, 61, 400)
    max_horizontal_upper_lane = Line(106, 700, 130, 116)
    max_horizontal_lower_lane = Line(10, 795, 247, 223)

    cube = cube_detector.detect(frame)
    horizontal_lane, vertical_lane = LaneCalculator.get_lane_for_cube(frame, cube, max_left_lane, max_right_lane,
                                                                      max_horizontal_upper_lane, max_horizontal_lower_lane)

    assert 2 == horizontal_lane
    assert -1 == vertical_lane



def test_bottom_lane_3():
    cube_detector = CubeDetector()
    frame = cv2.imread("../anki_object_detection/images/cube_up_lane_3.jpg")

    max_left_lane = Line(294, 181, 68, 415)
    max_right_lane = Line(490, 654, 61, 400)
    max_horizontal_upper_lane = Line(106, 700, 130, 116)
    max_horizontal_lower_lane = Line(10, 795, 247, 223)

    cube = cube_detector.detect(frame)
    horizontal_lane, vertical_lane = LaneCalculator.get_lane_for_cube(frame, cube, max_left_lane, max_right_lane,
                                                                      max_horizontal_upper_lane, max_horizontal_lower_lane)

    assert 3 == horizontal_lane
    assert -1 == vertical_lane



def test_bottom_lane_4():
    cube_detector = CubeDetector()
    frame = cv2.imread("../anki_object_detection/images/cube_up_lane_4.jpg")

    max_left_lane = Line(294, 181, 68, 415)
    max_right_lane = Line(490, 654, 61, 400)
    max_horizontal_upper_lane = Line(106, 700, 130, 116)
    max_horizontal_lower_lane = Line(10, 795, 247, 223)

    cube = cube_detector.detect(frame)
    horizontal_lane, vertical_lane = LaneCalculator.get_lane_for_cube(frame, cube, max_left_lane, max_right_lane,
                                                                      max_horizontal_upper_lane, max_horizontal_lower_lane)

    assert 4 == horizontal_lane
    assert -1 == vertical_lane
