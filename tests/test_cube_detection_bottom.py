import cv2 as cv2
from anki_object_detection.cube_detector import CubeDetector
from anki_object_detection.lane_calculator import LaneCalculator
from anki_object_detection.line import Line


def test_bottom_lane_1():
    cube_detector = CubeDetector()
    frame = cv2.imread("../anki_object_detection/images/camera_top_bottom_1.jpg")

    max_left_lane = Line(306, 312, 5, 486)
    max_right_lane = Line(484, 496, 2, 481)
    max_horizontal_upper_lane = Line(154, 638, 154, 143)
    max_horizontal_lower_lane = Line(157, 646, 337, 328)

    cube = cube_detector.detect(frame)
    horizontal_lane, vertical_lane = LaneCalculator.get_lane_for_cube(frame, cube, max_left_lane, max_right_lane,
                                              max_horizontal_upper_lane, max_horizontal_lower_lane)

    #cv2.namedWindow('test', cv2.WINDOW_NORMAL)
    #cv2.imshow('test', frame)
    #cv2.waitKey(0)

    assert 1 == horizontal_lane
    assert -1 == vertical_lane


def test_bottom_lane_2():
    cube_detector = CubeDetector()
    frame = cv2.imread("../anki_object_detection/images/camera_top_bottom_2.jpg")

    max_left_lane = Line(306, 312, 5, 486)
    max_right_lane = Line(484, 496, 2, 481)
    max_horizontal_upper_lane = Line(154, 638, 154, 143)
    max_horizontal_lower_lane = Line(157, 646, 337, 328)

    cube = cube_detector.detect(frame)
    horizontal_lane, vertical_lane = LaneCalculator.get_lane_for_cube(frame, cube, max_left_lane, max_right_lane,
                                                                      max_horizontal_upper_lane, max_horizontal_lower_lane)

    #cv2.namedWindow('test', cv2.WINDOW_NORMAL)
    #cv2.imshow('test', frame)
    #cv2.waitKey(0)

    assert 2 == horizontal_lane
    assert -1 == vertical_lane



def test_bottom_lane_3():
    cube_detector = CubeDetector()
    frame = cv2.imread("../anki_object_detection/images/camera_top_bottom_3.jpg")

    max_left_lane = Line(306, 312, 5, 486)
    max_right_lane = Line(484, 496, 2, 481)
    max_horizontal_upper_lane = Line(154, 638, 154, 143)
    max_horizontal_lower_lane = Line(157, 646, 337, 328)

    cube = cube_detector.detect(frame)
    horizontal_lane, vertical_lane = LaneCalculator.get_lane_for_cube(frame, cube, max_left_lane, max_right_lane,
                                                                      max_horizontal_upper_lane, max_horizontal_lower_lane)
    cv2.namedWindow('test', cv2.WINDOW_NORMAL)
    cv2.imshow('test', frame)
    cv2.waitKey(0)


    assert 3 == horizontal_lane
    assert -1 == vertical_lane



def test_bottom_lane_4():
    cube_detector = CubeDetector()
    frame = cv2.imread("../anki_object_detection/images/camera_top_bottom_4.jpg")

    max_left_lane = Line(306, 312, 5, 486)
    max_right_lane = Line(484, 496, 2, 481)
    max_horizontal_upper_lane = Line(154, 638, 154, 143)
    max_horizontal_lower_lane = Line(157, 646, 337, 328)

    cube = cube_detector.detect(frame)
    horizontal_lane, vertical_lane = LaneCalculator.get_lane_for_cube(frame, cube, max_left_lane, max_right_lane,
                                                                      max_horizontal_upper_lane, max_horizontal_lower_lane)

    assert 4 == horizontal_lane
    assert -1 == vertical_lane
